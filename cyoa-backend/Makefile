.PHONY: list

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

install_pipenv:
	pip install pipenv

install_dependencies:
	pipenv install --dev

setup_dependencies: install_pipenv install_dependencies

install_db:
	echo "DB: Using SQLite"

migrate_db:
	pipenv run ./manage.py migrate

setup_db: install_db migrate_db

setup_seed:
	echo "Seed: TBD"

remove_dependencies:
	pipenv --rm

remove_db:
	pipenv run ./manage.py flush

check_style:
	pipenv run pylint **/*.py

check_types:
	pipenv run mypy **/*.py

check_tests:
	pipenv run ./manage.py test

clean: remove_db remove_dependencies

setup: setup_dependencies setup_db setup_seed

install: install_dependencies

migrate: migrate_db

lint: check_style check_types

test: check_tests

check: lint test

build: setup check

shell:
	pipenv shell

start: migrate
	pipenv run ./manage.py runserver

all: build start
