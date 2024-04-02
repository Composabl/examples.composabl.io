import argparse
import os

import grpc
from composabl_core.grpc.server.server import Server
from server_impl import ServerImpl


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("HOST") or "[::]")
    parser.add_argument("--port", default=os.environ.get("PORT") or 1337, type=int)
    parser.add_argument(
        "--timeout", default=os.environ.get("TIMEOUT") or None, type=int
    )
    args = parser.parse_args()

    print(f"Starting with arguments {args}")

    try:
        server = Server(ServerImpl, args.host, args.port, args.timeout)
        server.start()
    except KeyboardInterrupt:
        print("KeyboardInterrupt, Gracefully stopping the server")
        server.stop()
    except grpc.RpcError as e:
        print(f"gRPC error: {e}, Gracefully stopping the server")
        server.stop()
    except Exception as e:
        print(f"Unknown error: {e}, Gracefully stopping the server")
        server.stop()


if __name__ == "__main__":
    start()
