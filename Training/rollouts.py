import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np
from time import time
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
    env1 = Zonk()
    score = deque(maxlen=500)
    n = 0
    start = time()
    while True:
        n+=1
        s, info = env.reset()
        episode = []
        total_reward = 0
        terminated = False
        while not terminated:
            pos_moves = len(info['possible_moves'])
            if pos_moves > 1:
                for i in range(100):
                    st, info1 = env1.reset(options={"state": env.get_state()})
                    episode1 = []
                    terminated1 = terminated
                    pos_moves1 = len(info1["possible_moves"])
                    while not terminated1:
                        a = agent.action(st, pos_moves1, optimal=False)
                        st1, r, terminated1, truncated1, info1 = env1.step(a)
                        terminated1 = terminated1 or truncated1
                        transition = (st, a, r, st1, pos_moves1)
                        episode1.append(transition)
                        st = st1
                        pos_moves1 = len(info1['possible_moves'])
                    agent.update(episode1)

            a = agent.action(s, pos_moves, optimal=True)
            s1, r, terminated, truncated, info = env.step(a)
            terminated = terminated or truncated
            transition = (s, a, r, s1, pos_moves)
            episode.append(transition)
            total_reward += r
            s = s1

        score.append(total_reward)
        agent.update(episode)
        if n % 500 == 0:
            print(f'На обучении: {sum(score) / len(score)}, Скорость: {time()-start}')
            start = time()


if __name__ == '__main__':
    main()
