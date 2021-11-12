help: ## Shows this help
	@echo "$$(grep -h '#\{2\}' $(MAKEFILE_LIST) | sed 's/: #\{2\} /	/' | column -t -s '	')"

install: ## Install the project using 'poetry' to manage virtual environment and packages
	poetry install

deps:
	poetry update

test: ## Run test suite
	python -m unittest

lint: ## Check for lint problems
	poetry run black --check .
	poetry run flake8 .
	poetry run mypy .

