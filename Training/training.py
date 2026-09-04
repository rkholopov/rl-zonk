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
    return parser.parse_args()


args = parse_args()

agent_map = {
        'MonteCarlo': MonteCarlo,
        'MonteCarloWIS': MonteCarloWIS,
        'CrossEntropy': CrossEntropy,
        'Baseline': Baseline,
        'QLearning': QLearning
    }

agent_class = agent_map[args.agent]

if args.soft != "Sampling":
    soft = float(args.soft)

agent = agent_class(soft=soft, alpha=args.alpha, percentile=args.percentile)
env = Zonk()

score = []
n = 0
while n <= args.episodes:
    n += 1

    s, info = env.reset()
    pos_moves = len(info['possible_moves'])
    a = agent.action(s, pos_moves)
    s1, r, terminated, info = env.step(a)
    episode = [(s, a, r, s1, pos_moves)]
    total_reward = r

    while not(terminated):
        s = s1
        pos_moves = len(info['possible_moves'])
        a = agent.action(s, pos_moves)
        s1, r, terminated, info = env.step(a)
        episode.append((s, a, r, s1, pos_moves))

        total_reward += r

    score.append(total_reward)
    agent.update(episode)

    if len(score) > args.eval_interval:
        score.pop(0)

    if n % args.eval_interval == 0:
        score1 = []
        for i in range(args.eval_episodes):
            s, info = env.reset()
            pos_moves = len(info['possible_moves'])
            a = agent.action(s, pos_moves, optimal=True)
            s1, r, terminated, info = env.step(a)
            episode = [(s, a, r, s1, pos_moves)]
            total_reward = r

            while not (terminated):
                s = s1
                pos_moves = len(info['possible_moves'])
                a = agent.action(s, pos_moves, optimal=True)
                s1, r, terminated, info = env.step(a)
                episode.append((s, a, r, s1, pos_moves))

                total_reward += r

            score1.append(total_reward)

        print(f'На обучении: {sum(score)/len(score)}, На инференсе: {sum(score1)/len(score1)}')
