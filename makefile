# Default input arguments
port ?= 8000

.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY run-dev
run-dev:
	fastapi dev main.py --port=$(port)