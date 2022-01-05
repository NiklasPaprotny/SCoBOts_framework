from tqdm import tqdm
import random
import time
from xrl.agents import Agent
from xrl.environments import agym
import gym
from xrl.agents.image_extractors import ColorExtractor, IColorExtractor, ZWhatClassifier
from xrl.agents.policies import RandomPolicy
from parsers import parser


def run_agent(agent, env, render=False):
    """
    run the agent in environment provided and return the reward.
    """
    _, tot_return = env.reset(), 0
    observation, reward, done, info = env.step(1)
    if render:
        env.render()
    for t in tqdm(range(3000)):
        action = agent(observation)
        observation, reward, done, info = env.step(action)
        tot_return += reward
        if render:
            env.render()
            time.sleep(0.1)
        if done:
            print(tot_return)
            break

args = parser.parse_args()
# game = ["Carnival", "MsPacman", "Pong", "SpaceInvaders", "Tennis"][1]
game = args.game
game_full_name = game + "Deterministic-v4"
if args.ari:
    env = agym.make(game_full_name)
else:
    env = gym.make(game_full_name)
random.seed(0)
env.seed(0)
if args.interactive:
    ice = IColorExtractor(game=game, load=False)
    agent = Agent([ice,
                   RandomPolicy(env.action_space.n)])
else:
    agent = Agent([ColorExtractor(game=game, load=False),
                   ZWhatClassifier(32, nb_class=10),
                   RandomPolicy(env.action_space.n)])

print(agent)
run_agent(agent, env, render=args.render)
if args.interactive:
    ice.save()