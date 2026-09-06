# dev-toolkit-21

`dev-toolkit-21` is a robust Python utility suite designed to streamline everyday development workflows and automate repetitive CLI tasks. It provides a modular foundation for file management, system diagnostics, and environment configuration across cross-platform projects.

## Features

*   **Project Scaffolder:** Rapidly generate standardized directory structures and boilerplate configuration files for new Python projects.
*   **System Diagnostics:** Quickly analyze environment variables, installed dependencies, and system path integrity to debug common configuration drift.
*   **File Streamliner:** Automated batch renaming and cleanup utilities for clearing build artifacts or temporary cache directories.
*   **Environment Sync:** Securely sync local `.env` templates across distributed team members without exposing sensitive credentials.

## Installation

Ensure you have Python 3.9+ installed. You can install the toolkit via pip:

```bash
# Clone the repository
git clone https://github.com/Developer/dev-toolkit-21.git
cd dev-toolkit-21

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

## Usage

Once installed, you can access the toolkit directly from your terminal. 

**Quick Scaffolding:**
Generate a new project structure in your current directory:

```bash
dev-toolkit scaffold --name my-new-project --template basic
```

**System Diagnostic Check:**
Run a health check on your current environment:

```bash
dev-toolkit diagnose --verbose
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.