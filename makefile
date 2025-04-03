# Default input arguments
port ?= 8000
docker ?= docker
image ?= public.ecr.aws/eodh/eodh-stac-validator
version ?= 0.1.0

.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY: run-dev
run-dev:
	fastapi dev main.py --port=$(port)

.PHONY: test
test:
	python -m pytest -v .

.PHONY: requirements
requirements:
	uv export --no-dev -q -o requirements.txt

.PHONY: container-build
container-build: requirements
	$(docker) build -t $(image):$(version) .

.PHONY: container-run
container-run: container-build
	$(docker) run --rm -p $(port):8000 $(image):$(version)

.PHONY: container-push
container-push:
	$(docker) push $(image):$(version)

.PHONY: publish
publish: container-build container-push