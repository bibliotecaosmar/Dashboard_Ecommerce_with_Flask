.PHONY: install init format lint test sec

install:
	@poetry install

init:
	@poetry add --dev black
	@poetry add --dev isort
	@poetry add --dev prospector
	@poetry add --dev pip-audit
	@poetry add --dev pytest
	@poetry add --dev pytest-cov

format:
	@isort .
	@black .

lint:
	@poetry run black . --check
	@poetry run isort . --check
	@poetry run prospector --with-tool pep257 --doc-warning

test:
	@poetry run pytest -v
	@poetry run pytest --cov=app tests/

sec:
	@poetry run pip-audit