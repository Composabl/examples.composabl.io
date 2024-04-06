import argparse
import random
from rllib.goals.RevenueUtilGoal import RevenueUtilGoal
from rllib.goals.DecorationStationUtilGoal import DecorationStationUtilGoal

from rllib.goals.MixerUtilGoal import MixerUtilGoal
from .log import Log
from ray.rllib.algorithms.callbacks import DefaultCallbacks, MultiCallbacks
import ray
from ray.rllib.algorithms import dqn
from simulation.recipe import RecipeNames
from rllib.action_mask_model import ActionMaskModel
from rllib.whisky_business_env import WhiskeyBusinessEnv

"""
-------------------------- Parse debug argument ----------------------------------------------
"""
parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug", type=bool, default=False, help="Use debug flag."
)
"""
-------------------------- Setting up Dynamic Cost ----------------------------------------------
"""
def dynamic_cost(recipeName) -> int:
    if recipeName == RecipeNames.cookies:
        cost = random.randint(5,10)
    if recipeName == RecipeNames.cupcakes:
        cost = random.randint(7,15)
    if recipeName == RecipeNames.cake:
        cost = random.randint(20,50)
    return cost

reward_fn = callable

"""
-------------------------- Setting up Machine Teaching ----------------------------------------------
"""
bakery_reward = MixerUtilGoal.reward_fn

class Machine_Teaching(DefaultCallbacks):
    def __init__(self):
        self.goals = [MixerUtilGoal, DecorationStationUtilGoal, RevenueUtilGoal]
        self.active_goal = self.goals[0]

    def on_episode_created(self, worker, base_env, policies, env_index, episode, **kwargs):
        worker.env.cookies_price = dynamic_cost(RecipeNames.cookies)
        worker.env.cake_price = dynamic_cost(RecipeNames.cake)
        worker.env.cupcake_price = dynamic_cost(RecipeNames.cupcakes)

    def on_episode_step(self, worker,base_env,policies,episode,env_index, **kwargs):
        goal_metric = []
        for goal in self.goals:
            goal_metric.append([goal.__name__, (goal.step_metric(goal,worker)/480)])

        self.goal_metric = goal_metric

    def on_episode_end(self, worker,base_env,policies,episode,env_index,**kwargs):       
        for goal_metric in self.goal_metric:
            episode.custom_metrics["episode_"+str(goal_metric[0])+"_metric"] = goal_metric[1]
    
    def on_evaluate_end(self, algorithm, evaluation_metrics, **kwargs):
        goal_success = []
        for goal in self.goals:
            goal_success.append(goal.episode_success(goal,evaluation_metrics["evaluation"]["custom_metrics"]["episode_" + str(goal.__name__) + "_metric_mean"]))

        for i, goal in enumerate(goal_success):
            if goal == False:
                self.active_goal = self.goals[i]

        
        bakery_reward = self.active_goal.reward_fn

        algorithm.workers.foreach_worker(
            lambda ev: ev.foreach_env(
                lambda env: env.set_reward_fn(bakery_reward)))

"""
-------------------------- Set up algorithm -----------------------------------------------
"""
ray.init()

args = parser.parse_args()

dqn_config = {
    "env_config": {
        "debug": args.debug
    }
}

config = (
            dqn.DQNConfig()
            .environment(
                WhiskeyBusinessEnv,
                env_config=dqn_config)
            .training(   
                hiddens=[],
                dueling=False,
                model={
                    "custom_model": ActionMaskModel
                }
            )
            .evaluation(
                evaluation_interval=2,
                evaluation_duration=2,
                evaluation_num_workers=2,
                evaluation_parallel_to_training=True,
            )
            .callbacks(MultiCallbacks(
                [Machine_Teaching,
                Log]
    
            ) )
        )

algo = config.build()

"""
-------------------------- Run train ----------------------------------------------
"""

for i in range(1000):
    result = algo.train()

    if i % 50 == 0:
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}")