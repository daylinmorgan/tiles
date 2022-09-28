## lint | lint.*
.PHONY: lint
lint: lint.py lint.sh

## lint.py | run black/flake8
.PHONY: lint.py
lint.py:
	@black tiles/ ./colors/colors.py
	@flake8 tiles

## lint.sh | run shfmt
.PHONY: lint.sh
lint.sh:
	@shfmt -w -s $(shell shfmt -f .)

-include .task.mk
$(if $(wildcard .task.mk),,.task.mk: ; curl -fsSL https://raw.githubusercontent.com/daylinmorgan/task.mk/v22.9.28/task.mk -o .task.mk)
