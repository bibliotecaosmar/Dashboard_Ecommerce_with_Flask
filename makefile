.PHONY: install init format lint test sec

install:
	@poetry install

run:
	@poetry run python run.py

migrate:
	@poetry run flask db init
	@poetry run flask db migrate
	@poetry run flask db upgrade

init:
	@poetry add --dev prospector
	@poetry add --dev pip-audit
	@poetry add --dev pytest -s
	@poetry add --dev pytest-cov

format:
	@isort .
	@black .

lint:
	@poetry run prospector --with-tool pydocstyle --doc-warning

test:
	@poetry run pytest -vs
	@poetry run pytest --cov=app tests/

sec:
	@poetry run pip-audit