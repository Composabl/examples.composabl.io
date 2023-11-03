import composabl_core.utils.logger as logger_util
from composabl_core.grpc.client.client import make

logger = logger_util.get_logger(__name__)

# Run: composabl sim start sim-starship --stream
logger.info("Creating Client for Simulator")
c = make(
    "run-benchmark",
    "sim-benchmark",
    "",
    "localhost:52075", # set the correct port
    {"render_mode": "rgb_array"},
)

logger.info("Initializing")
c.init()

logger.info("Resetting")
res = c.reset()

print(res)
