import argparse
import asyncio
import os

from composabl_core.grpc.server import ServerAsync
from server_impl import ServerImpl


async def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("HOST") or "[::]")
    parser.add_argument("--port", default=os.environ.get("PORT") or 1337, type=int)
    parser.add_argument(
        "--timeout", default=os.environ.get("TIMEOUT") or None, type=int
    )
    args = parser.parse_args()

    print(f"Starting with arguments {args}")

    try:
        server = ServerAsync(ServerImpl, args.host, args.port, args.timeout)
        await server.start()
    except Exception as e:
        print(f"Unknown error: {e}, Gracefully stopping the server")
        server.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
