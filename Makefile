ARGS = $(filter-out $@,$(MAKECMDGOALS))


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

sure: lint isort

tox:
	tox

test_on:
	pytest --cov=beethoven --cov-append --cov-report html:coverage_html -vs ${ARGS}

tests:
	pytest --cov=beethoven --cov-append --cov-report html:coverage_html -vs
.PHONY: tests

cov:
	pytest --cov=beethoven

cov_html:
	pytest --cov=beethoven --cov-report html:coverage_html

pdbg:
	apt update --yes
	apt install --yes inotify-tools

dbg:
	while :; do inotifywait beethoven/theory/* tests/theory/* beethoven/sequencer/* tests/sequencer/* beethoven/prompt/* tests/prompt/*;clear;pytest -vvs;done

clean:
	rm -rf coverage_html
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf
