import dotenv
from logging import WARNING, getLogger
import os

import uvicorn

from nightsservice.application import init_app
from nightsservice.config import PORT

dotenv.load_dotenv()
logger = getLogger(__name__)


def main(
    port: int,
) -> None:
    """Entry-point to service
    :param port The port to run on
    """
    logger.warning(f"Starting service on port {port}")

    uvicorn.run(
        "nightsservice.__main__:app",
        host="0.0.0.0",
        port=port,
        log_level=WARNING,
    )


if __name__ == "__main__":
    port = os.environ.get("PORT") or PORT
    main(port=int(port))
else:
    app = init_app()
