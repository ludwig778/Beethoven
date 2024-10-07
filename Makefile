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
	poetry run python3 -m flake8 beethoven

isort:
	poetry run python3 -m isort .

black:
	poetry run black --line-length 105 .

mypy:
	poetry run mypy ${ARGS}

piprot:
	poetry run piprot pyproject.toml

format: isort black
sure: tests lint mypy piprot
check: lint mypy piprot

debug:
	while :; do inotifywait -e modify -r .;clear;make ${ARGS};sleep .1 ;done

tests:
	poetry run pytest ${TEST_ARGS}

test_on:
	poetry run pytest ${TEST_ARGS} ${ARGS}

cov:
	poetry run pytest ${TEST_ARGS} --cov=beethoven

cov_html:
	poetry run pytest ${TEST_ARGS} --cov=beethoven --cov-report html:coverage_html

clean: build_clean
	rm -rf coverage_html .coverage .mypy_cache .pytest_cache
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf

build_clean:
	rm -rf build dist Beethoven.spec

convert_png_to_icns:
	poetry run icnsutil c ${ARGS}

build: build_clean
	poetry run pyinstaller \
		--name Beethoven \
		--icon "beethoven/ui/resources/icon/beethoven.icns" \
		--add-data "beethoven/ui/resources/img:img" \
		--windowed beethoven/ui/main.py

# Only on Mac, needs brew install create-dmg
build_mac: build
	create-dmg \
		--volname "Beethoven" \
		--window-pos 390 160 \
		--app-drop-link 0 0 \
		--hdiutil-quiet \
		"dist/Beethoven.dmg" \
		"dist/Beethoven.app"

.PHONY: build tests
