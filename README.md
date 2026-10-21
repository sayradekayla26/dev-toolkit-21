# dev-toolkit-21

`dev-toolkit-21` is a robust collection of Python utilities designed to streamline common development workflows and automate repetitive CLI tasks. It provides a lightweight, modular interface to handle system operations, file processing, and environment management with minimal overhead.

## Features

*   **Project Scaffolding:** Quickly generate standardized directory structures and configuration files for new Python projects.
*   **Log Auditor:** A structured logging wrapper that automatically rotates files and supports real-time filtering for debugging.
*   **Environment Sync:** A CLI utility to validate `.env` files against local templates and ensure required variables are defined.
*   **Resource Monitor:** Lightweight performance tracking for memory and CPU usage during long-running local scripts.

## Installation

Ensure you have Python 3.9+ installed. You can install the toolkit via pip:

```bash
pip install dev-toolkit-21
```

To install from source for development:

```bash
git clone https://github.com/Developer/dev-toolkit-21.git
cd dev-toolkit-21
pip install -e .
```

## Usage

After installation, you can access the toolkit via the `dtk` command-line interface.

**Generating a new project structure:**
```bash
dtk init --name my-new-app --template standard
```

**Validating your environment variables:**
```bash
dtk env-check --file .env --template .env.example
```

**Running a script with resource monitoring:**
```bash
dtk monitor --command "python main.py"
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.