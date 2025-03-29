# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import json
import aiohttp
from composabl_core import PerceptorImpl


OPENAI_KEY = "INSERT_KEY_HERE"
OPENAI_ENDPOINT = "https://YOUR_PROJECT.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT/completions?api-version=2024-03-01-preview"


class PerceptorOpenAI(PerceptorImpl):
    def __init__(self, observation_space, action_space):
        self.client = aiohttp.ClientSession()
        self.observation_space = observation_space
        self.action_space = action_space

    def _generate_prompt(self, obs_spec, obs):
        return f'In reinforcement learning and as pure JSON {{key:value}} (e.g., {{"is_landed": True}}), Based on the Observation Space `{str(obs_spec)}` and our Observation `{obs}` we can detect the following unique keys with their respective values that can be generated: {{'

    async def compute(self, obs_spec, obs):
        obs_spec = str(obs_spec).replace("\n", "").replace(" ", "")

        # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
        async with self.client.post(
            OPENAI_ENDPOINT,
            data=json.dumps(
                {
                    "prompt": self._generate_prompt(obs_spec, obs),
                    "temperature": 0,
                    "top_p": 1,
                    "frequency_penalty": 0,
                    "presence_penalty": 0,
                    "max_tokens": 100,
                    "stop": ["}"],  # We stop once it generated the end of the JSON
                    "stream": False,
                    "best_of": 1,
                }
            ),
            headers={
                "api-key": OPENAI_KEY,
                "Content-Type": "application/json",
            },
        ) as res:
            res = await res.json()

            if "choices" in res and len(res["choices"]) > 0:
                text = res["choices"][0]["text"]
                text_formatted = f"{text}}}"

                try:
                    return json.loads(text_formatted)
                except Exception:
                    return {}

        return {}

    def filtered_observation_space(self, obs):
        return ["counter"]
