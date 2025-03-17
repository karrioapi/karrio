# Karrio Carrier Integration Scripts

This document explains the scripts available in the root directory for working with carrier integrations.

## Available Scripts

### Creating a New Carrier

```bash
./create-carrier.sh [carrier_name] "[Display Name]"
```

Example:
```bash
./create-carrier.sh fedex_custom "FedEx Custom"
```

This script creates a complete carrier integration, including:
- Directory structure
- Boilerplate code
- JSON schema definitions
- Python type generation
- Package installation
- Initial tests

### Troubleshooting a Carrier

```bash
./troubleshoot-carrier.sh [carrier_name]
```

Example:
```bash
./troubleshoot-carrier.sh boxknight
```

This script helps diagnose common issues with carrier integrations, checking:
- Python version
- Karrio installation
- Carrier package installation
- Generate script existence and permissions
- Schema files existence
- Test files existence
- CLI tool availability
- Python dependencies

### Starting the Documentation Server

```bash
./start-docs.sh
```

This script starts the documentation server for carrier integrations. The documentation is available at http://localhost:8080.

### Running All Tests

```bash
./run-all-tests.sh [options]
```

Options:
- `--verbose true/false`: Run tests in verbose mode (default: true)
- `--coverage true/false`: Run tests with coverage (default: false)

Example:
```bash
./run-all-tests.sh --coverage true
```

This script runs tests for all carrier integrations and provides a summary of the results.

## Directory Structure

These scripts are wrappers around the scripts in the `plugins/boxknight/docs` directory. They allow you to run the scripts from any directory, making it more convenient to work with carrier integrations.

## Typer CLI Tool

We've created a powerful CLI tool using Typer, similar to the official Karrio CLI. To use it, run:

```bash
cd /path/to/karrio && ./bin/setup-karrio-path.sh
```

This will add the Karrio bin directory to your PATH, allowing you to run the following commands from anywhere:

```bash
karrio [command] [options]
```

Available commands:

- `karrio create-carrier [carrier_name] [display_name]` - Create a new carrier integration
- `karrio troubleshoot [carrier_name]` - Troubleshoot a carrier integration
- `karrio start-docs` - Start the documentation server
- `karrio run-tests [--verbose/--no-verbose] [--coverage/--no-coverage]` - Run all tests

For more information about a specific command, run:

```bash
karrio [command] --help
```

For example:

```bash
karrio create-carrier --help
```

## Troubleshooting

If you encounter any issues with these scripts, make sure:
1. The BoxKnight plugin is installed correctly
2. The scripts in `plugins/boxknight/docs` are executable
3. You have the necessary permissions to run the scripts

For more detailed information, see the documentation at http://localhost:8080 (run `./start-docs.sh` to start the server). 