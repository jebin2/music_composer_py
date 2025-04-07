#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
VENV_DIR="venv"
SYSTEM_DEPS_FILE="requirements-system.txt"

# --- Helper Functions ---
print_info() {
    echo "INFO: $1"
}

print_error() {
    echo "ERROR: $1" >&2
    exit 1
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_error "$1 command not found. Please install it first."
    fi
}

# --- Pre-flight Checks ---
print_info "Checking required commands..."
check_command "git"
check_command "python3"
# Check pip associated with python3
if ! python3 -m pip --version &> /dev/null; then
    print_error "pip for python3 not found. Please ensure pip is installed for your python3 environment."
fi

# --- System Dependency Installation ---
print_info "Installing system dependencies..."
if [ -f "$SYSTEM_DEPS_FILE" ]; then
    if command -v apt-get &> /dev/null; then
        print_info "Detected Debian/Ubuntu. Using apt-get..."
        sudo apt-get update
        sudo xargs -a "$SYSTEM_DEPS_FILE" apt-get install -y --no-install-recommends
    elif command -v brew &> /dev/null; then
        print_info "Detected macOS. Using brew..."
        # Read deps line by line in case xargs behaves differently or isn't preferred
        while IFS= read -r dep || [ -n "$dep" ]; do
          if [ -n "$dep" ]; then # Ensure line is not empty
            brew install "$dep"
          fi
        done < "$SYSTEM_DEPS_FILE"
    else
        print_error "Unsupported package manager. Please manually install dependencies listed in $SYSTEM_DEPS_FILE."
    fi
    print_info "System dependencies installed."
else
    print_error "$SYSTEM_DEPS_FILE not found. Cannot install system dependencies."
fi

# --- Python Virtual Environment Setup ---
if [ ! -d "$VENV_DIR" ]; then
    print_info "Creating Python virtual environment in '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
else
    print_info "Virtual environment '$VENV_DIR' already exists. Skipping creation."
fi

# --- Activate Virtual Environment (within script scope) ---
print_info "Activating virtual environment for installation..."
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# --- Install Python Dependencies ---
print_info "Upgrading pip and installing project dependencies from setup.py..."
pip install --upgrade pip setuptools wheel
pip install -e . # Install the project in editable mode and its dependencies

# --- Completion ---
# --- ANSI Escape Codes for Styling ---
BOLD=$(tput bold)
RESET=$(tput sgr0)
print_info "Installation complete!"
echo ""
echo "${BOLD}==================== Next Steps ====================${RESET}"
echo ""
echo "  1. ${BOLD}source venv/bin/activate${RESET}"
echo ""
echo "  2. ${BOLD}Create the .env file${RESET} in the project root:"
echo "     Create a file named '.env' and add your Google API key:"
echo "     ${BOLD}GOOGLE_API_KEY=your_google_gemini_api_key${RESET}"
echo ""
echo "  3. ${BOLD}python -m music_composer.web_server${RESET}"
echo ""
echo "${BOLD}===================================================${RESET}"

exit 0