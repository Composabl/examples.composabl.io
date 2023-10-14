from composabl_core.grpc.client import client


def start():
    # Examples
    # * CartPole-v1
    # * Hopper-v3
    # should be Hopper-v3 soon
    c = client.make("run-demo", "sim-demo", "Hopper-v3", "localhost:1337", {})
    c.init()

    print(c.observation_space_info())
    print(c.action_space_info())

if __name__ == "__main__":
    start()
