.PHONY: help dev build package clean

# Default target
help:
	@echo "BrushsetMaker - Available Commands:"
	@echo "  make dev       - Run the app in development mode"
	@echo "  make build     - Build the application for macOS"
	@echo "  make package   - Package the application as a .dmg"
	@echo "  make clean     - Remove all build artifacts and cached files"

# Run the app in development mode
dev:
	uv run briefcase dev

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
