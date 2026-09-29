# dev-toolkit-21

`dev-toolkit-21` is a robust command-line utility designed to streamline repetitive development workflows. It provides a suite of high-performance modules for file manipulation, environment validation, and automated project scaffolding.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Features

*   **Project Scaffolder:** Instantly initialize standardized project structures with pre-configured `.gitignore`, `README.md`, and `requirements.txt` files.
*   **Environment Validator:** Automatically scan your current directory for missing environment variables and dependency conflicts.
*   **Bulk File Refactor:** Perform mass renaming and string replacements across complex directory trees using RegEx-based pattern matching.
*   **Log Purger:** Securely clear stale cache files and temporary build artifacts to reclaim disk space with a single command.

### Installation

Ensure you have Python 3.8+ installed. You can install the toolkit directly via pip:

```bash
pip install dev-toolkit-21
```

Alternatively, for development use, clone the repository and install in editable mode:

```bash
git clone https://github.com/Developer/dev-toolkit-21.git
cd dev-toolkit-21
pip install -e .
```

### Basic Usage

Once installed, use the `dtk` command to interface with the toolkit. To initialize a new project structure in the current directory:

```bash
dtk init --name my-new-project
```

To run a health check on your existing environment dependencies:

```bash
dtk validate --env
```

To perform a bulk string replacement across all `.py` files in your project:

```bash
dtk refactor --pattern "OldClassName" --replace "NewClassName" --ext .py
```

### Contributing

Contributions are welcome! Please open an issue to discuss proposed changes or submit a pull request with unit tests for any new features.

### License

Distributed under the MIT License. See `LICENSE` for more information.