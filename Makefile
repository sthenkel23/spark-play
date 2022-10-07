SHELL := /usr/bin/env bash

IMAGE := spark_play
VERSION := latest

.PHONY: download-poetry
download-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python

.PHONY: install
install:
	poetry env use python3.10
	poetry lock -n
	poetry install -n
	

.PHONY: check-safety
check-safety:
	poetry check$(POETRY_COMMAND_FLAG) && \
	poetry run pip check$(PIP_COMMAND_FLAG) && \
	poetry run safety check --full-report$(SAFETY_COMMAND_FLAG) 

.PHONY: gitleaks
gitleaks:
	commits="$$(git rev-list --ancestry-path $$(git rev-parse $$(git branch -r --sort=committerdate | tail -1))..$$(git rev-parse HEAD))"; \
	if [ "$${commits}" != "" ]; then docker run --rm -v $$(pwd):/code/ zricethezav/gitleaks --path=/code/ -v --commits=$$(echo $${commits} | paste -s -d, -); fi;

.PHONY: check-style
check-style:
	poetry run black --config pyproject.toml ./$(BLACK_COMMAND_FLAG) && \
	poetry run darglint -v 2 **/*.py$(DARGLINT_COMMAND_FLAG) && \
	poetry run isort --settings-path pyproject.toml --check-only **/*.py$(ISORT_COMMAND_FLAG) 
# && \
# poetry run mypy --config-file setup.cfg src tests/**/*.py$(MYPY_COMMAND_FLAG)

.PHONY: format-code
format-code:
	poetry run pre-commit run

.PHONY: testing
testing:
	poetry run pytest --cov=src/$(IMAGE) tests/*.py

.PHONY: test
test: testing check-style check-safety


.PHONY: lint
lint: 
	poetry run pylint --disable=C src/${IMAGE}/*.py

# Example: make docker VERSION=latest
# Example: make docker IMAGE=some_name VERSION=0.1.0
.PHONY: docker
docker:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		   --build-arg PREFECT_API_KEY=${PREFECT_API_KEY} \
	       --build-arg PREFECT_ACCOUNT_ID=${PREFECT_ACCOUNT_ID} \
	       --build-arg PREFECT_WORKSPACE_ID=${PREFECT_WORKSPACE_ID} \
		   --build-arg PREFECT_QUEUE=${PREFECT_QUEUE} \
		   --build-arg FLOW_ENTRYPOINT=${FLOW_ENTRYPOINT} \
		   --build-arg APP_NAME=${APP_NAME} \
		-t $(IMAGE):$(VERSION) . \
		-f ./Dockerfile --no-cache

# Example: make clean_docker VERSION=latest
# Example: make clean_docker IMAGE=some_name VERSION=0.1.0
.PHONY: clean_docker
clean_docker:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)

.PHONY: clean_build
clean_build:
	rm -rf build/

.PHONY: clean
clean: clean_build clean_docker