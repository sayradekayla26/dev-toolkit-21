# dev-toolkit-21

`dev-toolkit-21` is a robust collection of Python utilities designed to streamline common development workflows and environment automation. This toolkit reduces boilerplate by consolidating file management, system diagnostics, and API orchestration into a single, modular interface.

## Features

*   **Environment Sync:** Effortlessly synchronize local `.env` variables across multiple project directories to maintain configuration consistency.
*   **Log Auditor:** A high-performance log parsing engine that extracts actionable insights and error patterns from raw development logs.
*   **System Profiler:** Real-time monitoring of local resource utilization, specifically tailored to identify memory leaks during Python script execution.
*   **Dependency Auditor:** Quickly cross-reference installed packages against known vulnerability databases for automated security posture checks.

## Installation

Ensure you have Python 3.9+ installed. Install the toolkit directly from the repository using pip:

```bash
git clone https://github.com/Developer/dev-toolkit-21.git
cd dev-toolkit-21
pip install -r requirements.txt
```

## Basic Usage

The toolkit provides a command-line interface for executing tasks. To scan your current project directory for potential security vulnerabilities, run:

```bash
python main.py audit --path ./my-project --level high
```

For a comprehensive diagnostic report of your system's current performance, use the profiler module:

```bash
python main.py profile --target cpu --duration 60
```

To view all available commands and configuration options, execute:

```bash
python main.py --help
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.