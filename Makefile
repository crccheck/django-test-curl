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

# 1. bump version in pyproject.toml
# 2. run `make publish`
# 3. git commit -am "0.0.0"
# 4. git tag "v0.0.0"
# 5. git push origin master --tags
publish: ## Publish to PyPI
	[ "$$(git rev-parse --abbrev-ref HEAD)" == "master" ]
	git pull
	poetry publish --build
