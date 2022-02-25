ARGS = $(filter-out $@,$(MAKECMDGOALS))

TEST_ARGS= -vvss

default: prompt

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
	while :; do inotifywait -e modify -r .;clear;make tests;sleep .1 ;done

tests:
	pytest ${TEST_ARGS}

test_on:
	pytest ${TEST_ARGS} ${ARGS}

cov:
	pytest ${TEST_ARGS} --cov=hartware_lib

cov_html:
	pytest ${TEST_ARGS} --cov=hartware_lib --cov-report html:coverage_html

clean:
	rm -rf coverage_html .coverage .mypy_cache .pytest_cache
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf

.PHONY: tests