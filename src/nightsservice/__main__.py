from logging import WARNING, getLogger

import uvicorn

from nightsservice.application import init_app
from nightsservice.config import PORT

logger = getLogger(__name__)


def main(
    port: int = PORT,
) -> None:
    """Entry-point to service
    :param port The port to run on
    """
    logger.warning("Starting service")

    uvicorn.run(
        "nightsservice.__main__:app",
        host="0.0.0.0",
        port=port,
        log_level=WARNING,
    )


if __name__ == "__main__":
    main()
else:
    app = init_app()
