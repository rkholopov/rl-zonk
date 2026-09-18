import unittest
from itertools import combinations
import numpy as np

from Enviroment.Zonk import Zonk
from Agents.CrossEntropy import CrossEntropy
from Training.training import run_episode


class RegressionTests(unittest.TestCase):
    def test_two_triples(self):
        for left, right in combinations(range(1, 7), 2):
            with self.subTest(left=left, right=right):
                env = Zonk()
                env.state = ('Choose cubes', 0, *([left] * 3 + [right] * 3))
                action = env.find_possible_moves().index('111111')
                state, reward, done, _ = env.step(action)
                expected = (1000 if left == 1 else left * 100) + right * 100
                self.assertEqual(reward, expected)
                self.assertEqual(state, ('Stop/Continue', 6, expected))
                self.assertFalse(done)

    def test_pairs_and_invalid_extra_dice(self):
        for dice, legal in [((2, 2, 3, 3, 4, 4), True),
                            ((2, 2, 3, 3, 3, 3), False),
                            ((2, 2, 2, 2, 3, 3), False)]:
            env = Zonk()
            env.state = ('Choose cubes', 0, *dice)
            moves = env.find_possible_moves()
            self.assertEqual('111111' in moves, legal)
            if legal:
                self.assertEqual(env.step(moves.index('111111'))[1], 750)

    def test_cross_entropy_retains_exploration(self):
        agent = CrossEntropy(0.1, 0.3, 85)
        agent.rng = np.random.default_rng(42)
        agent.policy[('state',)] = np.array([10., 0.])
        actions = [agent.action(('state',), 2) for _ in range(1000)]
        self.assertIn(1, actions)
        self.assertEqual(agent.action(('state',), 2, optimal=True), 0)
        self.assertEqual(agent.action(('unseen',), 2, optimal=True), 0)

    def test_evaluation_does_not_change_training(self):
        for cls in (CrossEntropy,):
            agents = [cls(0.1, 0.3, 85) for _ in range(2)]
            envs = [Zonk(seed=42), Zonk(seed=42)]
            for agent in agents:
                agent.rng = np.random.default_rng(42)
            for _ in range(30):
                episodes = [run_episode(env, agent) for env, agent in zip(envs, agents)]
                self.assertEqual(episodes[0], episodes[1])
                for agent, (episode, _) in zip(agents, episodes):
                    agent.update(episode)
                run_episode(Zonk(seed=7), agents[0], optimal=True)


if __name__ == '__main__':
    unittest.main()
