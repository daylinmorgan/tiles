lint: lint.py lint.sh ## lint.*

lint.py: ## run black/flake8
	@black tiles/ colors.py
	@pdm run ruff tiles colors.py

lint.sh: ## run shfmt
	@shfmt -w -s $(shell shfmt -f .)

-include .task.cfg.mk .task.mk
$(if $(wildcard .task.mk),,.task.mk: ; curl -fsSL https://raw.githubusercontent.com/daylinmorgan/task.mk/v23.1.1/task.mk -o .task.mk)
