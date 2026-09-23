import numpy as np
from collections import deque
from Agents.Monte_Carlo import MonteCarlo
from Agents.MonteCarloWIS import MonteCarloWIS
from Agents.CrossEntropy import CrossEntropy
from Agents.Baseline import Baseline
from Agents.QLearning import QLearning
from Enviroment.Zonk import Zonk


def main():
    agent_map = {
        'MonteCarlo': MonteCarlo,
        'MonteCarloWIS': MonteCarloWIS,
        'CrossEntropy': CrossEntropy,
        'Baseline': Baseline,
        'QLearning': QLearning,
    }
    soft = 0.3
    alpha = 0.1
    percentile = 85
    agent = MonteCarloWIS(soft=soft, alpha=alpha, percentile=percentile)
    env = Zonk()
    score = deque(maxlen=500)
    n = 0
    while True:
        n+=1
        s, info = env.reset()
        episode = []
        total_reward = 0
        terminated = False
        while not terminated:
            pos_moves = len(info['possible_moves'])
            if pos_moves > 1:
                for i in range(75):
                    env1 = Zonk()
                    env1.state = env.state
                    env1.score = env.score
                    episode1 = episode.copy()
                    st = s
                    terminated1 = terminated
                    pos_moves1 = pos_moves
                    while not terminated1:
                        a = agent.action(st, pos_moves1, optimal=False)
                        st1, r, terminated1, info1 = env1.step(a)
                        transition = (st, a, r, st1, pos_moves1)
                        episode1.append(transition)
                        st = st1
                        pos_moves1 = len(info1['possible_moves'])
                    agent.update(episode1)

            a = agent.action(s, pos_moves, optimal=True)
            s1, r, terminated, info = env.step(a)
            transition = (s, a, r, s1, pos_moves)
            episode.append(transition)
            total_reward += r
            s = s1

        score.append(total_reward)
        agent.update(episode)
        if n % 500 == 0:
            print(f'На обучении: {sum(score) / len(score)}')


if __name__ == '__main__':
    main()
