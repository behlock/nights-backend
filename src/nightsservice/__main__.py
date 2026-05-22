from __future__ import annotations

import dotenv
import uvicorn

from nightsservice.application import init_app
from nightsservice.logging_config import configure_logging
from nightsservice.settings import get_app_settings


def main() -> None:
    settings = get_app_settings()
    configure_logging(level=settings.LOG_LEVEL, is_production=settings.is_production)

    uvicorn.run(
        "nightsservice.__main__:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=False,
    )


dotenv.load_dotenv()
app = init_app()


if __name__ == "__main__":
    main()
