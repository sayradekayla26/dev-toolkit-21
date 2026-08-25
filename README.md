# dev-toolkit-21

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

dev-toolkit-21 is a Python toolkit that provides practical command-line utilities for daily development work. It focuses on reducing repetitive setup tasks and helping maintain consistent project standards across Python codebases.

## Features

- Scaffold new projects with a clean layout, pytest, ruff, and pre-commit configuration
- Run combined code quality checks including linting, type checking, and security scanning
- Audit dependencies and generate update suggestions while respecting existing constraints
- Create and manage isolated virtual environments with common development tools pre-installed

## Installation

```bash
pip install dev-toolkit-21
```

To install from source:

```bash
git clone https://github.com/Developer/dev-toolkit-21.git
cd dev-toolkit-21
pip install -e .
```

## Usage

Initialize a new project:

```bash
dev-toolkit init my-project
cd my-project
```

Run quality checks on the current project:

```bash
dev-toolkit check
```

## License

MIT License