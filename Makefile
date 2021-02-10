sh:
	bash

lint:
	python3 -m flake8

isort:
	python3 -m isort .

sure: lint isort

test:
	pytest -vs

cov:
	pytest --cov=beethoven

coverage:
	pytest --cov=beethoven --cov-report html:cov_html

pdbg:
	apt update --yes
	apt install --yes inotify-tools

dbg:
	while :; do inotifywait beethoven/theory/* tests/theory/* beethoven/sequencer/* tests/sequencer/*;clear;pytest -vs;done

clean:
	find . -name "*.pyc"|xargs rm
	find . -name "__pycache__"|xargs rm -rf
	rm -rf cov_html
