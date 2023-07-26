import argparse
import asyncio
import os

import composabl_ray.utils.logger as logger_util
import grpc
from boilerplate.server_impl import ServerImpl
from composabl_ray.server.server import Server

logger = logger_util.get_logger(__name__)


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("HOST") or "[::]")
    parser.add_argument("--port", default=os.environ.get("PORT") or 1337, type=int)
    parser.add_argument(
        "--timeout", default=os.environ.get("TIMEOUT") or None, type=int
    )
    args = parser.parse_args()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    logger.log(f"Starting with arguments {args}")

    try:
        server = Server(ServerImpl, args.host, args.port, args.timeout)
        event_loop.run_until_complete(server.start())
    except KeyboardInterrupt:
        logger.log("KeyboardInterrupt, Gracefully stopping the server")
        event_loop.run_until_complete(server.stop())
    except grpc.RpcError as e:
        logger.log(f"gRPC error: {e}, Gracefully stopping the server")
        event_loop.run_until_complete(server.stop())
    except Exception as e:
        logger.log(f"Unknown error: {e}, Gracefully stopping the server")
        event_loop.run_until_complete(server.stop())
