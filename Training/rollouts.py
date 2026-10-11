import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import numpy as np
from time import time
from collections import deque
from Agents.Monte_Carlo import MonteCarlo
from Agents.MonteCarloWIS import MonteCarloWIS
from Agents.CrossEntropy import CrossEntropy
from Agents.Baseline import Baseline
from Agents.QLearning import QLearning
from Enviroment.Zonk import Zonk


def parse_args():
    parser = argparse.ArgumentParser(description='Обучение Zonk с роллаутами')
    parser.add_argument('--agent', default='QLearning',
                        choices=['MonteCarlo', 'MonteCarloWIS', 'CrossEntropy', 'Baseline', 'QLearning'])
    parser.add_argument('--soft', default='0.1', help='Число от 0 до 1 или Sampling')
    parser.add_argument('--alpha', type=float, default=0.3)
    parser.add_argument('--percentile', type=float, default=85)
    parser.add_argument('--episodes', type=int, default=None,
                        help='Число реальных эпизодов; без параметра запуск бесконечный')
    parser.add_argument('--rollouts', type=int, default=100,
                        help='Число симуляций перед действием; 0 отключает симуляции')
    parser.add_argument('--log_interval', type=int, default=500,
                        help='Частота вывода и размер окна средней награды')
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()
    if args.soft != 'Sampling':
        try:
            args.soft = float(args.soft)
        except ValueError:
            parser.error('--soft должен быть числом от 0 до 1 или Sampling')
        if not 0 <= args.soft <= 1:
            parser.error('--soft должен быть от 0 до 1')
    if not 0 < args.alpha <= 1 or not 0 <= args.percentile <= 100:
        parser.error('0 < alpha <= 1, 0 <= percentile <= 100')
    if args.episodes is not None and args.episodes < 0:
        parser.error('--episodes должен быть неотрицательным')
    if args.rollouts < 0 or args.log_interval <= 0:
        parser.error('rollouts >= 0, log_interval > 0')
    if args.seed is not None and args.seed < 0:
        parser.error('--seed должен быть неотрицательным')
    return args


def main():
    args = parse_args()
    agent_map = {
        'MonteCarlo': MonteCarlo,
        'MonteCarloWIS': MonteCarloWIS,
        'CrossEntropy': CrossEntropy,
        'Baseline': Baseline,
        'QLearning': QLearning,
    }
    agent = agent_map[args.agent](soft=args.soft, alpha=args.alpha, percentile=args.percentile)
    if hasattr(agent, 'rng'):
        agent.rng = np.random.default_rng(args.seed)
    env = Zonk(seed=args.seed)
    rollout_seed = None if args.seed is None else args.seed + 1
    env1 = Zonk(seed=rollout_seed)
    score = deque(maxlen=args.log_interval)
    n = 0
    start = time()
    while args.episodes is None or n < args.episodes:
        n+=1
        s, info = env.reset()
        episode = []
        total_reward = 0
        terminated = False
        while not terminated:
            pos_moves = len(info['possible_moves'])
            if pos_moves > 1:
                for i in range(args.rollouts):
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
        if n % args.log_interval == 0 or n == args.episodes:
            print(f'Эпизод: {n}, На обучении: {sum(score) / len(score)}, Время блока (с): {time()-start:.2f}')
            start = time()


if __name__ == '__main__':
    main()
