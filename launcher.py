#! /bin/python3

import os

# Retrieve the environment variable 'COMPOSABL_EULA_AGREED'
eula_agreed = os.getenv('COMPOSABL_EULA_AGREED')

# Check if the environment variable is set and print its value or a message indicating it's not set
if eula_agreed == '1' :
    print(f"COMPOSABL_EULA_AGREED: {eula_agreed}")
else:
    print("The environment variable 'COMPOSABL_EULA_AGREED' is not set.")
    # Print a message asking for a Yes or No input
    print("Do you agree to the terms? (Yes/No)")

    # Capture the user's input
    user_input = input()

    # Check the user's input and print a corresponding message
    if user_input.lower() == 'yes':
        print("You have agreed to the terms.")
    elif user_input.lower() == 'no':
        print("You have not agreed to the terms.")
        exit()
    else:
        print("Invalid input. Please respond with 'Yes' or 'No'.")
        exit()

    # Set the environment variable 'COMPOSABL_EULA_AGREED'
    os.environ['COMPOSABL_EULA_AGREED'] = '1'

    # Verify that the environment variable is set
    eula_agreed = os.getenv('COMPOSABL_EULA_AGREED')
    print(f"COMPOSABL_EULA_AGREED is now set to: {eula_agreed}")

import subprocess
# Check if the environment variable 'COMPOSABL_LICENSE' is set
composabl_license = os.getenv('COMPOSABL_LICENSE')
if not composabl_license:
    print("COMPOSABL_LICENSE is not set.")
    print( "you must get a license from Compsosabl and EXPORT it as an environment variable")
else:
    print("license is set" )


import json

def generate_config(license_key, target, image, env_name, workers, num_gpus):
    # Assuming this function generates a configuration dictionary based on the input parameters
    return {
        "target": target,
        "image": image,
        "env_name": env_name,
        "workers": workers,
        "num_gpus": num_gpus
    }

"""
# Path to your JSON file
user_story_json_file_path = './rocket_landing/agents/config.json'

# Read the JSON file into a dictionary
try:
    with open(user_story_json_file_path, 'r') as file:
        config_data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file '{user_story_json_file_path}' was not found.")
except json.JSONDecodeError:
    print(f"Error: The file '{user_story_json_file_path}' is not a valid JSON file.")
# Handle other potential exceptions, such as permission errors
except Exception as e:
    print(f"An unexpected error occurred: {e}")
  """

import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description="Process some inputs.")

# Define positional arguments
parser.add_argument("command", type=str, help="The command to execute")
parser.add_argument("name", type=str, help="The name associated with the command")

# Define optional arguments
parser.add_argument("--workers", type=int, help="Number of workers", default=1)
parser.add_argument("--num_gpus", type=int, help="Number of GPUs", default=0)

# Parse the arguments
args = parser.parse_args()

# Use the arguments
print(f"Command: {args.command}")
print(f"Name: {args.name}")
print(f"Workers: {args.workers}")
print(f"Number of GPUs: {args.num_gpus}")


import subprocess


# This line ensures that the function runs only when the script is executed directly,python
# and not when imported as
#  a module.
if __name__ == '__main__':
    print( 'foo')
    if args.command =='teach':
        print(f'run {args.name}')
        cur_dir=os.getcwd()
        agent_dir=f'{cur_dir}/{args.name}'
        print(agent_dir)
        os.chdir( agent_dir)
        result = subprocess.call(["python3","agent.py"])
        print(result)



