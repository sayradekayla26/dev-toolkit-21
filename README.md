# dev-toolkit-21

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

dev-toolkit-21 is a Python toolkit that provides practical command-line utilities for everyday development tasks. It helps developers initialize projects, manage environments, and handle common maintenance work with minimal setup.

## Features

- Scaffold new Python projects with standard directory structures and configuration files
- Create and validate virtual environments with automatic requirements checking
- Scan dependencies for outdated packages and known security vulnerabilities
- Generate boilerplate for tests, CLI entry points, and configuration files

## Installation

```bash
pip install dev-toolkit-21
```

Install from source:

```bash
git clone https://github.com/developer/dev-toolkit-21.git
cd dev-toolkit-21
pip install -e .
```

## Usage

Initialize a new project:

```bash
dev-toolkit init my-project --type cli
```

Audit dependencies:

```bash
dev-toolkit audit
```

View all available commands:

```bash
dev-toolkit --help
```