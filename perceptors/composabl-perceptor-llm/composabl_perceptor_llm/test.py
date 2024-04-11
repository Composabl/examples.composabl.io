# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from composabl_perceptor_llm.perceptor import PerceptorOpenAI
from gymnasium.spaces import Box
import numpy as np


async def start():
    p = PerceptorOpenAI(None, None)
    res = await p.compute(
        Box(
            np.array([-1.5, -1.5, -5.0, -5.0, -3.1415927, -5.0, -0.0, -0.0]),
            np.array([1.5, 1.5, 5.0, 5.0, 3.1415927, 5.0, 1.0, 1.0]),
            (8,),
            np.float32,
        ),
        {"counter": 1},
    )
    print(res)


if __name__ == "__main__":
    import asyncio

    asyncio.run(start())
