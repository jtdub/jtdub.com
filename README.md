# jtdub.com Development Environment

This repository contains the source code for [jtdub.com](https://www.jtdub.com), a Jekyll-based personal website. This guide will help you set up the development environment to work on the site locally.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker** - For running Jekyll in a containerized environment
- **Docker Compose** - For orchestrating the development environment
- **Python 3.11+** - For running development tools and tests
- **Poetry** - For Python dependency management

### Installing Prerequisites

#### macOS (using Homebrew)
```bash
# Install Docker Desktop (includes Docker Compose)
brew install --cask docker

# Install Python and Poetry
brew install python@3.11
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to your PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="$HOME/.local/bin:$PATH"
```

#### Ubuntu/Debian
```bash
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# Install Python and Poetry
sudo apt install python3.11 python3-pip
curl -sSL https://install.python-poetry.org | python3 -
```

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jtdub/jtdub.com.git
   cd jtdub.com
   ```

2. **Install Python dependencies:**
   ```bash
   poetry install
   ```

3. **Install Jekyll dependencies (first time only):**
   ```bash
   poetry run invoke bundle-install
   ```

4. **Start the development environment:**
   ```bash
   poetry run invoke start
   ```

5. **View your site:**
   Open http://localhost:4000 in your browser

6. **Stop the environment when done:**
   ```bash
   poetry run invoke stop
   ```

## Development Workflow

### Starting Development

```bash
# Start Jekyll with live reload
poetry run invoke start

# Or start and follow logs
poetry run invoke dev
```

Your site will be available at http://localhost:4000. Changes to your Jekyll files will automatically trigger a rebuild and reload in the browser.

### Making Changes

1. Edit Jekyll files (Markdown, HTML, CSS, etc.)
2. Changes are automatically detected and the site rebuilds
3. Refresh your browser to see changes
4. For major changes, you may need to restart: `poetry run invoke restart`

### Testing

```bash
# Run all tests
poetry run invoke test

# Run tests with coverage report
poetry run invoke test-coverage

# Run linting
poetry run invoke lint

# Format Python code
poetry run invoke format
```

## Available Commands

### Jekyll Environment Management

| Command | Description |
|---------|-------------|
| `poetry run invoke start` | Start Jekyll development server |
| `poetry run invoke stop` | Stop Jekyll development server |
| `poetry run invoke restart` | Restart Jekyll development server |
| `poetry run invoke dev` | Start server and follow logs |
| `poetry run invoke status` | Check container status |
| `poetry run invoke logs` | View container logs |

### Jekyll Build Tasks

| Command | Description |
|---------|-------------|
| `poetry run invoke build` | Build site without starting server |
| `poetry run invoke bundle-install` | Install Ruby gems |
| `poetry run invoke shell` | Open shell in Jekyll container |

### Testing and Code Quality

| Command | Description |
|---------|-------------|
| `poetry run invoke test` | Run pytest tests |
| `poetry run invoke test-coverage` | Run tests with coverage |
| `poetry run invoke lint` | Run ruff linter |
| `poetry run invoke format` | Format Python code |

### Cleanup

| Command | Description |
|---------|-------------|
| `poetry run invoke clean` | Clean up Docker containers and volumes |

## Project Structure

```
jtdub.com/
├── _config.yml              # Jekyll configuration
├── _data/                   # Data files
├── _includes/               # Reusable template parts
├── _layouts/                # Page layouts
├── _plugins/                # Custom Jekyll plugins
├── _posts/                  # Blog posts
├── _site/                   # Generated site (ignored)
├── assets/                  # CSS, JS, images
├── development/             # Development environment
│   ├── docker-compose.yml   # Docker Compose configuration
│   └── README.md            # Development environment docs
├── tests/                   # Test files
├── tasks.py                 # Invoke task definitions
├── pyproject.toml           # Python dependencies
└── Gemfile                  # Ruby dependencies
```

## Docker Environment Details

The development environment uses Docker to provide a consistent Jekyll setup across different machines. Key features:

- **Jekyll 4.2.0** - Matches the production environment
- **Live Reload** - Automatic rebuilding when files change
- **Port 4000** - Standard Jekyll development port
- **Volume Mounting** - Your local files are mounted into the container
- **Gem Persistence** - Ruby gems are cached between container restarts

## Writing Blog Posts

1. **Create a new post:**
   ```bash
   touch _posts/$(date +%Y-%m-%d)-your-post-title.md
   ```

2. **Add front matter:**
   ```markdown
   ---
   layout: post
   title: "Your Post Title"
   date: 2025-08-17 10:00:00 -0500
   tags: [tag1, tag2]
   ---
   
   Your post content here...
   ```

3. **Preview your post:**
   The development server will automatically show your new post at http://localhost:4000

## Troubleshooting

### Common Issues

**Port 4000 already in use:**
```bash
# Stop any existing Jekyll processes
poetry run invoke stop
# Or find and kill the process
lsof -ti:4000 | xargs kill -9
```

**Docker container won't start:**
```bash
# Clean up and restart
poetry run invoke clean
poetry run invoke start
```

**Ruby gems missing:**
```bash
# Reinstall gems
poetry run invoke bundle-install
```

**Python dependencies issues:**
```bash
# Reinstall Python dependencies
poetry install --no-cache
```

### Getting Help

If you encounter issues:

1. Check the container logs: `poetry run invoke logs`
2. Verify Docker is running: `docker ps`
3. Check the Jekyll build output for errors
4. Try cleaning and restarting: `poetry run invoke clean && poetry run invoke start`

## Contributing

1. Create a new branch for your changes
2. Make your modifications
3. Test your changes: `poetry run invoke test`
4. Ensure code quality: `poetry run invoke lint`
5. Start the development server to preview: `poetry run invoke start`
6. Submit a pull request

## Additional Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Invoke Documentation](https://www.pyinvoke.org/)

---

Happy coding! 🚀
