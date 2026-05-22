"""Legacy constants. Prefer ``nightsservice.settings.get_app_settings()``."""

from __future__ import annotations

from nightsservice.settings import get_app_settings

_settings = get_app_settings()
PORT = _settings.PORT
SERVICE_NAME = _settings.SERVICE_NAME
VERSION = _settings.VERSION
