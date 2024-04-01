# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import asyncio
from argparse import ArgumentParser

from composabl_core.networking import server as server_make

from server_impl import ServerImpl

async def start(host, port, protocol, env_init: dict = {}):
    server = server_make.make(
        server_impl=ServerImpl,
        host=host,
        port=port,
        protocol=protocol,
        env_init=env_init
    )

    await server.start()

    # Wait forever
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    # Create the parser
    parser = ArgumentParser(description="Start the server with specified arguments")

    # Add arguments for host, port, and protocol
    parser.add_argument("--host", default="0.0.0.0", help="Host address to bind the server to")
    parser.add_argument("--port", type=int, default=1337, help="Port number to bind the server to")
    parser.add_argument("--protocol", default="grpc", help="Protocol to use (e.g., grpc)")
    parser.add_argument("--env_init", type=str, default="{}", help="Environment initialization (e.g., {})")

    # Parse the arguments
    args = parser.parse_args()

    # Covnert from str to dict
    args.env_init = eval(args.env_init)

    # Run the start function with the parsed arguments
    asyncio.run(start(args.host, args.port, args.protocol, args.env_init))
