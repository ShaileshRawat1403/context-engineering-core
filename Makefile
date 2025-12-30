# Convenience commands for local development
.PHONY: test test-verbose check-structure diagrams clean build docs-build docs-serve docs-deploy

PYTEST ?= pytest
MKDOCS ?= mkdocs
export PYTHONWARNINGS ?= ignore::UserWarning:fs

test:
	$(PYTEST) -q

test-verbose:
	$(PYTEST) -vv

check-structure:
	$(PYTEST) -q tests/test_structure.py

diagrams:
	bash scripts/render_diagrams.sh

clean:
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	rm -rf .pytest_cache site

build: docs-build

docs-build:
	$(MKDOCS) build --clean --strict

docs-serve:
	$(MKDOCS) serve --watch-theme

docs-deploy:
	$(MKDOCS) gh-deploy --clean --force
