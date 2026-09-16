# dev-toolkit-21

`dev-toolkit-21` is a robust Python utility suite designed to streamline common developer workflows and automate repetitive local environment tasks. It provides a modular command-line interface to manage project scaffolding, cleanup, and file synchronization efficiently.

## Features

*   **Project Scaffolder:** Automatically generates standardized directory structures and configuration files for Python, Node.js, and shell projects.
*   **Environment Purger:** Quickly identifies and removes heavy build artifacts, `__pycache__` directories, and broken symlinks to reclaim disk space.
*   **Env-Sync Utility:** Securely manages and synchronizes `.env` templates across multiple development environments to ensure consistency.
*   **Smart Log Parser:** A regex-based utility for extracting critical error patterns from large production log files with zero dependencies.

## Installation

Ensure you have Python 3.8+ installed. You can install the toolkit directly via pip:

```bash
pip install dev-toolkit-21
```

Alternatively, for development mode, clone the repository and run:

```bash
git clone https://github.com/Developer/dev-toolkit-21.git
cd dev-toolkit-21
pip install -e .
```

## Usage

Once installed, use the `dtk` command to interact with the toolkit. To purge temporary build files in your current project directory:

```bash
dtk purge --target ./src
```

To initialize a new Python project structure:

```bash
dtk init --type python --name my-new-project
```

For a full list of available commands and configuration options, run:

```bash
dtk --help
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.