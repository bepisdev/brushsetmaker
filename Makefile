.PHONY: help dev build package clean

# Default target
help:
	@echo "BrushsetMaker - Available Commands:"
	@echo "  make dev       - Run the app in development mode"
	@echo "  make build     - Build the application for macOS"
	@echo "  make package   - Package the application as a .dmg"
	@echo "  make clean     - Remove all build artifacts and cached files"
	@echo "  make release   - Create a new release using git flow"
	@echo "  make setup		- Set up the development environment"

# Run the app in development mode
dev:
	uv run briefcase dev

# Set up the development environment
setup:
	./scripts/setup_dev.sh

# Create a new release using git flow
release:
	uv run scripts/bump_version.py
	uv run git add .
	uv run git commit -m "Bump version"
	git flow release finish

# Build the application
build:
	uv run briefcase build

# Package the application as .dmg
package: build
	uv run briefcase package

# Clean all build artifacts, caches, and gitignored files
clean:
	@echo "Cleaning build artifacts and cached files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type f -name "*.so" -delete 2>/dev/null || true
	rm -rf build/
	rm -rf dist/
	rm -rf venv/
	rm -rf env/
	rm -rf ENV/
	rm -rf .venv/
	rm -f uv.lock
	# IDE files
	rm -rf .vscode/
	rm -rf .idea/
	find . -type f -name "*.swp" -delete 2>/dev/null || true
	find . -type f -name "*.swo" -delete 2>/dev/null || true
	find . -type f -name "*~" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	@echo "Clean complete!"
