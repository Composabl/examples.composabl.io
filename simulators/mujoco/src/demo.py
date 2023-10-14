import cv2
from composabl_core.grpc.client import client

# python3 -m mujoco.viewer

def start():
    # Examples
    # * CartPole-v1
    # * Hopper-v3
    # should be Hopper-v3 soon
    c = client.make("run-demo", "sim-demo", "Walker2D", "localhost:1337", {})
    c.init()

    print(c.observation_space_info())
    print(c.action_space_info())

    # # Display the img
    # print(img)
    # cv2.imshow("Sheep", np.array(img))
    # cv2.waitKey(0)

if __name__ == "__main__":
    start()
