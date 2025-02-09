VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
MANAGE = $(PYTHON) manage.py

# Default target (run when you just type `make`)
all: run

# Set up the virtual environment and install dependencies if it doesn't exist
setup:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV); \
		echo "Installing dependencies..."; \
		$(PIP) install -r requirements.txt; \
	else \
		echo "Virtual environment already exists. Skipping setup."; \
	fi

# Run the Django development server
run: setup
	$(MANAGE) runserver

.PHONY: all setup run