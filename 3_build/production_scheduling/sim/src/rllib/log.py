from ray.rllib.algorithms.callbacks import DefaultCallbacks

class Log(DefaultCallbacks):

    def on_episode_end(self, worker,base_env,policies,episode,env_index,**kwargs):
        cookies_price = worker.env.cookies_price
        cupcakes_price = worker.env.cupcake_price
        cake_price = worker.env.cake_price

        completed_cookies = worker.env.current_state["completed_cookies"]
        completed_cupcakes = worker.env.current_state["completed_cupcakes"]
        completed_cake = worker.env.current_state["completed_cake"]

        print("Total Cookies ($",cookies_price,"): ", completed_cookies,
              ", Total Cupcakes ($",cupcakes_price,"): ", completed_cupcakes,
              ", Total Cakes ($",cake_price,"): ", completed_cake,
              ", Revenue - $", (cookies_price*completed_cookies) + (cupcakes_price*completed_cupcakes) + (cake_price*completed_cake),
              ", Reward -", episode.total_reward)        

    
    def on_evaluate_end(self, algorithm, evaluation_metrics, **kwargs):
        print("EVAL METRIC",evaluation_metrics)

        