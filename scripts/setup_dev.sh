#!/usr/bin/env bash
#
# Development Environment Setup Script for BrushsetMaker
#
# This script automates the setup of the development environment by:
# - Checking for required system tools
# - Installing missing Python tools (uv, ruff)
# - Setting up Python virtual environment with uv
# - Installing Python dependencies
# - Installing Ruby dependencies for documentation site
# - Verifying the installation
#
# Usage:
#   ./scripts/setup_dev.sh [--skip-ruby] [--skip-python] [--force]
#
# Options:
#   --skip-ruby    Skip Ruby/Jekyll setup
#   --skip-python  Skip Python environment setup
#   --force        Force reinstall even if tools are present
#   --help         Show this help message

set -e  # Exit on error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Script options
SKIP_RUBY=false
SKIP_PYTHON=false
FORCE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-ruby)
            SKIP_RUBY=true
            shift
            ;;
        --skip-python)
            SKIP_PYTHON=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --help)
            head -n 20 "$0" | grep "^#" | sed 's/^# //' | sed 's/^#//'
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Helper functions
print_header() {
    echo -e "\n${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

get_version() {
    case $1 in
        python|python3)
            python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'
            ;;
        ruby)
            ruby --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1
            ;;
        git)
            git --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'
            ;;
        uv)
            uv --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown"
            ;;
        ruff)
            ruff --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'
            ;;
        bundler)
            bundler --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'
            ;;
        make)
            make --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Main script
print_header "BrushsetMaker Development Environment Setup"

echo "This script will set up your development environment."
echo "It will check for required tools and install missing dependencies."
echo ""

# Check system requirements
print_header "Checking System Requirements"

MISSING_TOOLS=()

# Check git
if check_command git; then
    print_success "git $(get_version git) found"
else
    print_error "git not found"
    MISSING_TOOLS+=("git")
fi

# Check make
if check_command make; then
    print_success "make $(get_version make) found"
else
    print_error "make not found"
    MISSING_TOOLS+=("make")
fi

# Check for macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_success "Running on macOS"

    # Check for Xcode command line tools
    if xcode-select -p &> /dev/null; then
        print_success "Xcode command line tools installed"
    else
        print_warning "Xcode command line tools not found"
        print_info "Install with: xcode-select --install"
        MISSING_TOOLS+=("xcode-select")
    fi
else
    print_warning "Not running on macOS - some features may not work"
fi

# Check Python
if ! $SKIP_PYTHON; then
    print_header "Checking Python Environment"

    if check_command python3; then
        PYTHON_VERSION=$(get_version python3)
        print_success "Python $PYTHON_VERSION found"

        # Check Python version >= 3.12
        REQUIRED_VERSION="3.12"
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)" 2>/dev/null; then
            print_success "Python version meets requirements (>= $REQUIRED_VERSION)"
        else
            print_error "Python version $PYTHON_VERSION is too old (requires >= $REQUIRED_VERSION)"
            MISSING_TOOLS+=("python3.12+")
        fi
    else
        print_error "Python 3 not found"
        MISSING_TOOLS+=("python3")
    fi

    # Check uv
    if check_command uv; then
        UV_VERSION=$(get_version uv)
        print_success "uv $UV_VERSION found"
    else
        print_warning "uv not found - will install"
        if $FORCE || ! check_command uv; then
            print_info "Installing uv..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            # Add to PATH for current session
            export PATH="$HOME/.cargo/bin:$PATH"
            if check_command uv; then
                print_success "uv installed successfully"
            else
                print_error "Failed to install uv"
                MISSING_TOOLS+=("uv")
            fi
        fi
    fi

    # Check ruff
    if check_command ruff; then
        RUFF_VERSION=$(get_version ruff)
        print_success "ruff $RUFF_VERSION found"
    else
        print_warning "ruff not found - will install via uv"
    fi
fi

# Check Ruby
if ! $SKIP_RUBY; then
    print_header "Checking Ruby Environment"

    if check_command ruby; then
        RUBY_VERSION=$(get_version ruby)
        print_success "Ruby $RUBY_VERSION found"
    else
        print_error "Ruby not found"
        MISSING_TOOLS+=("ruby")
    fi

    if check_command bundler; then
        BUNDLER_VERSION=$(get_version bundler)
        print_success "bundler $BUNDLER_VERSION found"
    else
        print_warning "bundler not found - will install"
        if check_command gem; then
            print_info "Installing bundler..."
            gem install bundler --user-install
            if check_command bundler; then
                print_success "bundler installed successfully"
            else
                print_warning "bundler installation may need manual PATH configuration"
            fi
        else
            print_error "gem command not found - cannot install bundler"
            MISSING_TOOLS+=("bundler")
        fi
    fi
fi

# Exit if critical tools are missing
if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo ""
    print_error "Missing required tools: ${MISSING_TOOLS[*]}"
    echo ""
    echo "Please install the missing tools and try again."
    echo ""
    echo "Installation guides:"
    echo "  - git: https://git-scm.com/downloads"
    echo "  - Python 3.12+: https://www.python.org/downloads/"
    echo "  - Ruby: https://www.ruby-lang.org/en/documentation/installation/"
    echo "  - Xcode tools: xcode-select --install"
    echo "  - uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi

# Setup Python environment
if ! $SKIP_PYTHON; then
    print_header "Setting Up Python Environment"

    if check_command uv; then
        print_info "Creating/updating virtual environment with uv..."
        uv venv

        print_info "Installing Python dependencies with uv sync..."
        uv sync

        print_success "Python environment setup complete"

        # Install ruff if not present
        if ! check_command ruff; then
            print_info "Installing ruff..."
            uv pip install ruff
            print_success "ruff installed"
        fi

        # Verify installation
        print_info "Verifying Python installation..."
        if uv run python -c "import brushsetmaker; print(f'BrushsetMaker {brushsetmaker.__version__}')"; then
            print_success "BrushsetMaker package verified"
        else
            print_warning "Could not verify BrushsetMaker package"
        fi
    else
        print_error "uv not available - skipping Python setup"
    fi
fi

# Setup Ruby environment
if ! $SKIP_RUBY; then
    print_header "Setting Up Ruby Environment (Documentation)"

    if check_command bundler && [ -f "docs/Gemfile" ]; then
        print_info "Installing Ruby gems for Jekyll documentation..."
        cd docs
        bundle install
        cd ..
        print_success "Ruby gems installed"

        print_info "Verifying Jekyll installation..."
        if bundle exec jekyll --version &> /dev/null; then
            print_success "Jekyll verified"
        else
            print_warning "Could not verify Jekyll installation"
        fi
    else
        if [ ! -f "docs/Gemfile" ]; then
            print_warning "docs/Gemfile not found - skipping Ruby setup"
        else
            print_error "bundler not available - skipping Ruby setup"
        fi
    fi
fi

# Final summary
print_header "Setup Complete!"

echo "Development environment is ready. Here are some useful commands:"
echo ""
echo "  ${BOLD}Development:${NC}"
echo "    make dev              - Run the app in development mode"
echo "    make build            - Build the application"
echo "    make package          - Package as .dmg"
echo ""
echo "  ${BOLD}Documentation:${NC}"
echo "    cd docs && bundle exec jekyll serve"
echo "                          - Run documentation site locally"
echo ""
echo "  ${BOLD}Version Management:${NC}"
echo "    python scripts/bump_version.py --patch"
echo "                          - Bump version number"
echo ""
echo "  ${BOLD}Linting:${NC}"
echo "    ruff check .          - Check code style"
echo "    ruff format .         - Format code"
echo ""
echo "For more information, see docs/documentation/contribute/"
echo ""

print_success "Happy coding! 🚀"
