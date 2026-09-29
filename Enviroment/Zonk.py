import gymnasium as gym
from gymnasium import spaces
import numpy as np


class ScoreSpace(spaces.Space):
    def __init__(self):
        super().__init__(shape=(), dtype=object)

    def sample(self, mask=None, probability=None):
        if mask is not None or probability is not None:
            raise ValueError("ScoreSpace does not support masks")
        number_of_fifties = int(self.np_random.geometric(0.05)) - 1
        return 50 * number_of_fifties

    def contains(self, value):
        if type(value) is not int:
            return False
        if value < 0:
            return False
        return value % 50 == 0


class Zonk(gym.Env):
    DECISION = 0
    CHOOSE = 1
    TERMINAL = 2
    metadata = {"render_modes": []}

    def __init__(self, seed=None):
        super().__init__()

        self.action_space = spaces.Discrete(64)
        state_fields = [
            spaces.Discrete(3),
            ScoreSpace(),
            spaces.Discrete(7),
        ]
        for _ in range(6):
            state_fields.append(spaces.Discrete(7))
        self.observation_space = spaces.Tuple(state_fields)
        self._initial_seed = seed
        self._has_reset = False
        self.phase = self.DECISION
        self.score = 0
        self.num_dice = 6
        self.dice = ()

    def reset(self, *, seed=None, options=None):
        if seed is None and not self._has_reset:
            seed = self._initial_seed
        super().reset(seed=seed)
        self._has_reset = True
        state = (self.DECISION, 0, 6, 0, 0, 0, 0, 0, 0)
        if options is not None and "state" in options:
            state = options["state"]
        self._restore_state(state)
        return self.get_state(), self._info()

    def get_state(self):
        state = [self.phase, self.score, self.num_dice]
        state.extend(self.dice)
        while len(state) < 9:
            state.append(0)
        return tuple(state)

    def _restore_state(self, state):
        if not isinstance(state, tuple):
            raise ValueError("State must be a tuple")
        if not self.observation_space.contains(state):
            raise ValueError("State values are outside observation_space")

        phase = int(state[0])
        score = state[1]
        num_dice = int(state[2])
        dice = [int(value) for value in state[3:]]
        rolled_dice = []

        if phase == self.CHOOSE:
            if num_dice == 0:
                raise ValueError("Choose phase requires at least one die")
            rolled_dice = dice[:num_dice]
            if 0 in rolled_dice:
                raise ValueError("Rolled dice must have values from 1 to 6")
            if rolled_dice != sorted(rolled_dice):
                raise ValueError("Rolled dice must be sorted")
            unused_positions = dice[num_dice:]
        else:
            if phase == self.DECISION and num_dice == 0:
                raise ValueError("Decision phase requires at least one die")
            if phase == self.TERMINAL and num_dice != 0:
                raise ValueError("Terminal state must have zero dice")
            unused_positions = dice

        for value in unused_positions:
            if value != 0:
                raise ValueError("Unused dice positions must be zero")

        self.phase = phase
        self.score = score
        self.num_dice = num_dice
        self.dice = tuple(rolled_dice)

    def _info(self):
        moves = self.find_possible_moves()
        mask = np.zeros(64, dtype=np.int8)
        mask[:len(moves)] = 1
        return {"possible_moves": moves, "action_mask": mask}

    def _finish(self, reward, invalid=False):
        self.phase = self.TERMINAL
        self.num_dice = 0
        self.dice = ()
        info = self._info()
        if invalid:
            info["invalid_action"] = True
        return self.get_state(), reward, True, False, info

    def step(self, action):
        if not self._has_reset or self.phase == self.TERMINAL:
            raise gym.error.ResetNeeded("Call reset before stepping a new round")
        if not self.action_space.contains(action):
            raise ValueError("Action must be an integer in [0, 63]")
        moves = self.find_possible_moves()
        if action >= len(moves):
            return self._finish(-self.score, invalid=True)
        move = moves[int(action)]
        if move == '-1':
            if self.phase == self.DECISION:
                reward = 0
            else:
                reward = -self.score
            return self._finish(reward)
        if move == '0':
            roll = self.np_random.integers(1, 7, self.num_dice)
            rolled_dice = []
            for value in roll:
                rolled_dice.append(int(value))
            rolled_dice.sort()
            self.dice = tuple(rolled_dice)
            self.phase = self.CHOOSE
            reward = 0
        else:
            selected = self._selected_dice(move)
            reward = self._points(selected)
            if reward == 0:
                return self._finish(-self.score)
            self.score += reward
            self.num_dice -= len(selected)
            if self.num_dice == 0:
                self.num_dice = 6
            self.dice = ()
            self.phase = self.DECISION
        return self.get_state(), reward, False, False, self._info()

    def _selected_dice(self, move):
        selected = []
        for index, flag in enumerate(move):
            if flag == '1':
                selected.append(self.dice[index])
        return selected

    @staticmethod
    def _points(dice):
        counts = {}
        for face in range(1, 7):
            counts[face] = dice.count(face)

        points = 0
        for face, count in counts.items():
            if count >= 3:
                if face == 1:
                    triple_points = 1000
                else:
                    triple_points = face * 100

                points += triple_points * (count - 2)
            elif face == 1:
                points += count * 100
            elif face == 5:
                points += count * 50

        if dice == [1, 2, 3, 4, 5, 6]:
            return 1500
        if Zonk._is_three_pairs(dice):
            return max(points, 750)
        return points

    @staticmethod
    def _is_three_pairs(dice):
        if len(dice) != 6:
            return False
        pairs = 0
        for face in range(1, 7):
            if dice.count(face) == 2:
                pairs += 1
        return pairs == 3

    def find_possible_moves(self):
        if self.phase == self.TERMINAL:
            return []
        if self.phase == self.DECISION:
            if self.score >= 300:
                return ['-1', '0']
            return ['0']

        moves = ['-1']

        for selection_number in range(1, 2 ** self.num_dice):
            number = selection_number
            flags = []
            for _ in range(self.num_dice):
                flags.append(str(number % 2))
                number //= 2
            move = ''.join(flags)
            selected = self._selected_dice(move)

            valid = True
            for face in (2, 3, 4, 6):
                count = selected.count(face)
                if count == 1 or count == 2:
                    valid = False
                    break

            if selected == [1, 2, 3, 4, 5, 6]:
                valid = True
            if self._is_three_pairs(selected):
                valid = True
            if valid:
                moves.append(move)
        return moves
