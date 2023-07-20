#!/usr/bin/env sh
poetry run black $@ main.py models tests utils
