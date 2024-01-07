import argparse
import csv
import time
import uuid
import os
from datetime import datetime
from timeit import timeit
import logging

import numpy as np
from composabl_core.grpc.client import client

global_start_time = datetime.now()
session_id = str(uuid.uuid4())

def stop(start_time):
    end_time = datetime.now()
    delta = end_time-start_time
    total_seconds = delta.total_seconds()
    return total_seconds

def get_run_time():
    seconds = stop(global_start_time)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{hours}:{minutes}:{seconds}'

# def start_simple(power=2):
#     c = client.make(
#         "run-demo",
#         "sim-demo",
#         "Walker2D",
#         "localhost:1337",
#         # Set the env_init
#         # this gets passed to the env constructor as kwargs if they exist
#         {
#             # typically can be human, rgb_array, or depth_array
#             "render_mode": "rgb_array"
#         }
#     )

#     c.init()
#     c.reset()

#     max_range = 10**power

#     def sample_step(i):
#         #a = c.action_space_sample()
#         #c.step(a[0])
#         #print(i)
#         return

#     [sample_step(i) for i in range(max_range)]

def start(port_number=1,power=2,write_files=True):
    c = client.make(
        "run-demo",
        "sim-demo",
        "Walker2D",
        f"localhost:{port_number}",
        # Set the env_init
        # this gets passed to the env constructor as kwargs if they exist
        {
            # typically can be human, rgb_array, or depth_array
            "render_mode": "rgb_array"
        },
        True #async
    )

    c.init()
    c.reset()

    c_id = str(uuid.uuid4())
    fields = ['PortNumber','SessionID','ClientID','StepNo','MaxSteps','SampleTime','StepTime','Epoch']
    rows = []
    max_range = 10**power

    def sample_step(i):
        start_sample = datetime.now()
        a = c.action_space_sample()
        end_sample = stop(start_sample)
        start_step = datetime.now()
        c.ustep(a[0])
        end_step = stop(start_step)
        if write_files:
            rows.append([port_number,session_id, c_id, i, max_range, end_sample, end_step, time.time()])

    [sample_step(i) for i in range(max_range)]

    if write_files:
        file_name = f'/mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/profiled/{c_id}.csv'

        with open(file_name, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)

def run_timeit_profile(port_number,write_files=False):
    for i in range(3,4):
        func_name = 'start'
        func_call = f'{func_name}({port_number},{i},{write_files})'
        #for j in range(3,6):
        j = 2
        number = 10**j
        result = timeit(func_call, number=number, setup=f"from __main__ import {func_name}")
        print(f'Call ({i},{j}) averaged {result/number} seconds')

    print(f'Ran for {get_run_time()}')

if __name__ == "__main__":
    os.environ['PYTHONASYNCIODEBUG']="1"
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", default="1337")
    parser.add_argument("--write-files", default=False)
    args = parser.parse_args()

    print(f"Starting with arguments {args}")

    #logging.basicConfig(filename=f'logs/{args.client}-c.log', encoding='utf-8', level=logging.DEBUG)

    # logger = logging.getLogger()
    # #logging.basicConfig(filename=f'logs/{args.port}-s.log', encoding='utf-8', level=logging.DEBUG)
    # fh = logging.FileHandler(f'/mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/logs/{args.client}-c.log')
    # fh.setLevel(logging.DEBUG)
    # logger.addHandler(fh)


    #start_simple()
    #run_timer_profile()
    run_timeit_profile(args.client, args.write_files)
