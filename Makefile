ARGS = $(filter-out $@,$(MAKECMDGOALS))


TEST_ARGS= -vs


default: prompt

prompt:
	poetry run python3 beethoven/prompt/main.py

py:
	poetry run python3

sh:
	bash

lint:
	python3 -m flake8 beethoven/ tests/

isort:
	python3 -m isort beethoven/ tests/

mypy:
	mypy .

sure: lint isort mypy

test_on:
	pytest ${TEST_ARGS} ${ARGS}

tests:
	pytest ${TEST_ARGS}
.PHONY: tests

cov:
	pytest --cov=beethoven ${TEST_ARGS}

cov_html:
	pytest --cov=beethoven --cov-report html:coverage_html ${TEST_ARGS}

pdbg:
	apt update --yes
	apt install --yes inotify-tools

dbg:
	while :; do inotifywait beethoven/theory/* tests/theory/* beethoven/sequencer/* tests/sequencer/* beethoven/prompt/* tests/prompt/*;clear;pytest -vvs;done

clean:
	rm -rf coverage_html
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf
