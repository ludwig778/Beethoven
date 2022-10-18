ARGS = $(filter-out $@,$(MAKECMDGOALS))

TEST_ARGS= -vs --show-capture=no

default: ui

ui:
	poetry run python3 -m beethoven.ui

prompt:
	poetry run python3 beethoven/prompt/main.py

sh:
	bash

py:
	poetry run ipython3 ${ARGS}

lint:
	python3 -m flake8 .

isort:
	python3 -m isort .

black:
	poetry run black .

mypy:
	mypy .

piprot:
	piprot pyproject.toml

format: isort black
sure: tests lint mypy piprot

debug:
	while :; do inotifywait -e modify -r .;clear;make ${ARGS};sleep .1 ;done

tests:
	pytest ${TEST_ARGS}

test_on:
	pytest ${TEST_ARGS} ${ARGS}

cov:
	pytest ${TEST_ARGS} --cov=beethoven

cov_html:
	pytest ${TEST_ARGS} --cov=beethoven --cov-report html:coverage_html

clean:
	rm -rf coverage_html .coverage .mypy_cache .pytest_cache
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf

.PHONY: tests
