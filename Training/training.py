import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import argparse
from Agents.Monte_Carlo import MonteCarlo
from Agents.MonteCarloWIS import MonteCarloWIS
from Agents.CrossEntropy import CrossEntropy
from Agents.Baseline import Baseline
from Agents.QLearning import QLearning
from Enviroment.Zonk import Zonk


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', type=str, default='Baseline',
                        choices=['MonteCarlo', 'MonteCarloWIS', 'CrossEntropy', 'Baseline', 'QLearning'])
    parser.add_argument('--soft', type=str, default='0.1', help='Гиперпараметр для мягкой стратегии')
    parser.add_argument('--alpha', type=float, default=0.3, help='Скорость обучения QLearning')
    parser.add_argument('--percentile', type=float, default=85.0, help='Процент элитных проходов для CrossEntropy')
    parser.add_argument('--episodes', type=int, default=100000, help='Общее число эпизодов')
    parser.add_argument('--eval_interval', type=int, default=10000, help='Как часто оценивать')
    parser.add_argument('--eval_episodes', type=int, default=10000, help='Число эпизодов для оценки')
    parser.add_argument('--seed', type=int, default=None, help='Seed для воспроизводимого запуска')
    args = parser.parse_args()
    if args.soft != 'Sampling':
        try:
            args.soft = float(args.soft)
        except ValueError:
            parser.error('--soft должен быть числом от 0 до 1 или Sampling')
        if not 0 <= args.soft <= 1:
            parser.error('--soft должен быть от 0 до 1')
    if args.episodes < 0 or args.eval_interval <= 0 or args.eval_episodes <= 0:
        parser.error('episodes >= 0, eval_interval > 0, eval_episodes > 0')
    if not 0 < args.alpha <= 1 or not 0 <= args.percentile <= 100:
        parser.error('0 < alpha <= 1, 0 <= percentile <= 100')
    return args


def run_episode(env, agent, optimal=False):
    s, info = env.reset()
    episode = []
    total_reward = 0
    terminated = False
    while not terminated:
        pos_moves = len(info['possible_moves'])
        a = agent.action(s, pos_moves, optimal=optimal)
        s1, r, terminated, info = env.step(a)
        transition = (s, a, r, s1, pos_moves)
        episode.append(transition)
        total_reward += r
        s = s1
    return episode, total_reward


def main():
    from collections import deque
    import numpy as np

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
    eval_env = Zonk(seed=None if args.seed is None else args.seed + 1)
    score = deque(maxlen=args.eval_interval)
    for n in range(1, args.episodes + 1):
        episode, total_reward = run_episode(env, agent)
        score.append(total_reward)
        agent.update(episode)
        if n % args.eval_interval == 0:
            eval_scores = [run_episode(eval_env, agent, optimal=True)[1]
                           for _ in range(args.eval_episodes)]
            print(f'На обучении: {sum(score)/len(score)}, На инференсе: {sum(eval_scores)/len(eval_scores)}')


if __name__ == '__main__':
    main()
