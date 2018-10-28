help: ## Shows this help
	@echo "$$(grep -h '#\{2\}' $(MAKEFILE_LIST) | sed 's/: #\{2\} /	/' | column -t -s '	')"

test: ## Run test suite
	python -m unittest

lint: ## Check for lint errors
	flake8

publish: ## Publish to PyPI
	[ "$$(git rev-parse --abbrev-ref HEAD)" == "master" ]
	git pull
	poetry publish
