.PHONY: install init format lint test sec

install:
	@poetry install

init:
	@poetry add --dev prospector
	@poetry add --dev pip-audit
	@poetry add --dev pytest
	@poetry add --dev pytest-cov

format:
	@isort .
	@black .

lint:
	@poetry run prospector --with-tool pydocstyle --doc-warning

test:
	@poetry run pytest -v
	@poetry run pytest --cov=app tests/

sec:
	@poetry run pip-audit