.DEFAULT_GOAL := all
sources = shellrecharge

.PHONY: .pdm  ## Check that PDM is installed
.pdm:
	@pdm -V || echo 'Please install PDM: https://pdm.fming.dev/latest/\#installation'

.PHONY: .pre-commit  ## Check that pre-commit is installed
.pre-commit:
	@pre-commit -V || echo 'Please install pre-commit: https://pre-commit.com/'

.PHONY: install  ## Install the package, dependencies, and pre-commit for local development
install: .pdm .pre-commit
	pdm install --group :all
	pre-commit install --install-hooks

.PHONY: refresh-lockfiles  ## Sync lockfiles with requirements files.
refresh-lockfiles: .pdm
	pdm update --update-reuse --group :all

.PHONY: rebuild-lockfiles  ## Rebuild lockfiles from scratch, updating all dependencies
rebuild-lockfiles: .pdm
	pdm update --update-eager --group :all

.PHONY: format  ## Auto-format python source files
format: .pdm
	pdm run isort $(sources)
	pdm run black -l 79 $(sources)
	pdm run ruff format $(sources)

.PHONY: lint  ## Lint python source files
lint: .pdm
	pdm run ruff check $(sources)
	pdm run mypy $(sources)

.PHONY: codespell  ## Use Codespell to do spellchecking
codespell: .pre-commit
	pre-commit run codespell --all-files

.PHONY: publish  ## Publish to PyPi
publish: .pdm
	pdm build
	twine upload dist/*

.PHONY: all  ## Run the standard set of checks performed in CI
all: lint codespell

.PHONY: clean  ## Clear local caches and build artifacts
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name '*.py[co]' -exec rm -f {} +
	find . -type f -name '*~' -exec rm -f {} +
	find . -type f -name '.*~' -exec rm -f {} +
	rm -rf .cache
	rm -rf .mypy_cache
	rm -rf .pdm-build
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf site

.PHONY: help  ## Display this message
help:
	@grep -E \
		'^.PHONY: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".PHONY: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
