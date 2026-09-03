from Agents.Monte_Carlo import MonteCarlo
from Agents.MonteCarloWIS import MonteCarloWIS
from Agents.CrossEntropy import CrossEntropy
from Agents.Baseline import Baseline
from Agents.QLearning import QLearning
from Enviroment.Zonk import Zonk


agent = CrossEntropy(85)
env = Zonk()

score = []
n = 0
while True:
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

    if len(score)>10000:
        score.pop(0)

    if n%10000==0:
        score1 = []
        for i in range(10000):
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
