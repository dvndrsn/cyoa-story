.PHONY: list

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

install_pipenv:
	pip install pipenv

install:
	pipenv install

remove:
	pipenv --rm

setup: install_pipenv install

reset: remove setup

shell:
	pipenv shell

start:
	pipenv run ./manage.py runserver

lint:
	pipenv run pylint **/*.py

test:
	pipenv run ./manage.py test

verify: lint test

build: setup verify
