import cv2
from composabl_core.grpc.client import client
import numpy as np

env_names = [
    "ant",
    "half_cheetah",
    "hopper",
    "humanoid",
    "humanoidstandup",
    "inverted_double_pendulum",
    "inverted_pendulum",
    "pusher",
    "reacher",
    "swimmer",
    "walker2d"
]

def start():
    """
    This example creates a client that:
    1. Connects to the simulator
    2. Gets the initial frame after reset from each environment
    3. Displays all of the environments in a grid overview
    """
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

    env_screens = []

    # Render the different environments
    for i, env_name in enumerate(env_names):
        c = client.make(
            "run-demo",
            "sim-demo",
            env_name,
            "localhost:1337",
            # Set the env_init
            # this gets passed to the env constructor as kwargs if they exist
            {
                # typically can be human, rgb_array, or depth_array
                "render_mode": "rgb_array"
            }
        )

        c.init()

        # Reset the environment
        c.reset()

        # Get the initial frame
        img = c.get_render()
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Add the env_screen to the list
        env_screens.append(img_bgr)

    # Construct a grid from the env_screens
    env_screen_width = img_bgr.shape[1]
    env_screen_height = img_bgr.shape[0]

    grid_cols = 4
    grid_rows = 3

    grid_width = env_screen_width * grid_cols
    grid_height = env_screen_height * grid_rows

    grid = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    for i, env_screen in enumerate(env_screens):
        col = i % grid_cols
        row = i // grid_cols

        x = col * env_screen_width
        y = row * env_screen_height

        grid[y:y + env_screen_height, x:x + env_screen_width] = env_screen

    # Save the grid
    cv2.imwrite("grid.png", grid)


if __name__ == "__main__":
    start()
