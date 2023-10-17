import cv2
from composabl_core.grpc.client import client

# python3 -m mujoco.viewer

def start():
    # Examples
    # * CartPole-v1
    # * Hopper-v3
    # should be Hopper-v3 soon
    c = client.make(
        "run-demo",
        "sim-demo",
        "Walker2D",
        "localhost:1337",
        # Set the env_init
        # this gets passed to the env constructor as kwargs if they exist
        {
            # typically can be human, rgb_array, or depth_array
            "render_mode": "rgb_array"
        }
    )

    c.init()

    print(c.observation_space_info())
    print(c.action_space_info())

    # Walk through the environment and print
    for _episode_idx in range(5):
        print(f"episode {_episode_idx}")

        obs, _info = c.reset()
        for _step_index in range(1):
            a = c.action_space_sample()

            # Somehow the action is of type (1, 6) but it should be (6,)
            # this is specific to the walker
            a = a[0]

            # Step
            obs, _reward, done, _truncated, _info = c.step(a)
            print(obs)

            # Render
            img = c.get_render()
            print(img)
            # cv2.imshow(c.get_render())
            # cv2.waitKey(0)



    # # Display the img
    # print(img)
    # cv2.imshow("Sheep", np.array(img))
    # cv2.waitKey(0)

if __name__ == "__main__":
    start()
