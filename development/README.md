# Development Environment

This directory contains the Docker Compose configuration for local Jekyll development.

## Setup

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Install Ruby gems (first time only):**
   ```bash
   poetry run invoke bundle-install
   ```

## Available Commands

### Jekyll Development Environment

- **Start Jekyll server:**
  ```bash
  poetry run invoke start
  ```
  Site will be available at http://localhost:4000

- **Stop Jekyll server:**
  ```bash
  poetry run invoke stop
  ```

- **Restart Jekyll server:**
  ```bash
  poetry run invoke restart
  ```

- **View logs:**
  ```bash
  poetry run invoke logs
  ```

- **Check status:**
  ```bash
  poetry run invoke status
  ```

- **Start and show logs:**
  ```bash
  poetry run invoke dev
  ```

### Jekyll Build Tasks

- **Build site without server:**
  ```bash
  poetry run invoke build
  ```

- **Install Ruby gems:**
  ```bash
  poetry run invoke bundle-install
  ```

- **Open shell in container:**
  ```bash
  poetry run invoke shell
  ```

### Testing and Linting

- **Run tests:**
  ```bash
  poetry run invoke test
  ```

- **Run tests with coverage:**
  ```bash
  poetry run invoke test-coverage
  ```

- **Run linter:**
  ```bash
  poetry run invoke lint
  ```

- **Format code:**
  ```bash
  poetry run invoke format
  ```

### Cleanup

- **Clean up Docker environment:**
  ```bash
  poetry run invoke clean
  ```

## Quick Start

```bash
# Start development environment
poetry run invoke start

# View your site at http://localhost:4000
# Make changes to your Jekyll files - they'll auto-reload

# When done
poetry run invoke stop
```
