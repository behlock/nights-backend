#!/usr/bin/env sh
poetry run flake8 --max-line-length 99 main.py models tests utils
