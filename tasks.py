"""
Invoke tasks for managing the Jekyll development environment and running tests.

This task file focuses on Docker-based development to avoid Ruby version and
architecture compatibility issues. All Jekyll operations run in containerized
environments for consistency across different development machines and CI/CD.

Key commands:
- invoke setup: Full setup (install gems + build site)
- invoke quick-build: Build site without starting server
- invoke serve: Start development server with live reload
- invoke exec-jekyll '<command>': Run arbitrary commands in Jekyll container
- invoke add-platforms: Add Linux platform support for CI/CD
"""

import os
from invoke import task

# Path to the development directory containing docker-compose.yml
DEV_DIR = "development"
COMPOSE_FILE = os.path.join(DEV_DIR, "docker-compose.yml")


@task
def start(c):
    """Start the Jekyll development environment."""
    print("🚀 Starting Jekyll development environment...")
    with c.cd(DEV_DIR):
        c.run("docker-compose up -d")
    print("✅ Jekyll is now running at http://localhost:4000")


@task
def stop(c):
    """Stop the Jekyll development environment."""
    print("🛑 Stopping Jekyll development environment...")
    with c.cd(DEV_DIR):
        c.run("docker-compose down")
    print("✅ Jekyll development environment stopped")


@task
def restart(c):
    """Restart the Jekyll development environment."""
    print("🔄 Restarting Jekyll development environment...")
    stop(c)
    start(c)
    print("✅ Jekyll development environment restarted")


@task
def logs(c):
    """Show logs from the Jekyll container."""
    print("📋 Showing Jekyll container logs...")
    with c.cd(DEV_DIR):
        c.run("docker-compose logs -f jekyll")


@task
def status(c):
    """Show status of the Jekyll development environment."""
    print("📊 Checking Jekyll development environment status...")
    with c.cd(DEV_DIR):
        c.run("docker-compose ps")


@task
def shell(c):
    """Open a shell in the Jekyll container."""
    print("🐚 Opening shell in Jekyll container...")
    with c.cd(DEV_DIR):
        c.run("docker-compose exec jekyll /bin/bash")


@task
def build(c):
    """Build the Jekyll site without starting the server."""
    print("🔨 Building Jekyll site...")
    with c.cd(DEV_DIR):
        c.run("docker-compose run --rm jekyll jekyll build --trace")
    print("✅ Jekyll site built successfully")


@task
def bundle_install(c):
    """Install Ruby gems using Docker container."""
    print("💎 Installing Ruby gems in Docker container...")
    with c.cd(DEV_DIR):
        c.run("docker-compose run --rm jekyll bundle install")
    print("✅ Ruby gems installed successfully")


@task
def quick_build(c):
    """Quick build Jekyll site using Docker without starting server."""
    print("🔨 Building Jekyll site in Docker container...")
    with c.cd(DEV_DIR):
        c.run("docker-compose run --rm jekyll jekyll build")
    print("✅ Jekyll site built successfully")

    _run_jekyll_build(c, "")
    print("✅ Jekyll site built successfully")
@task
def setup(c):
    """Setup Jekyll environment (install gems and build) using Docker."""
    print("⚙️ Setting up Jekyll environment in Docker...")
    bundle_install(c)
    quick_build(c)
    print("✅ Jekyll environment setup complete")


@task
def add_platforms(c):
    """Add platform support for CI/CD environments using Docker."""
    print("🏗️ Adding platform support for CI/CD environments...")
    with c.cd(DEV_DIR):
        c.run("docker-compose run --rm jekyll bundle lock --add-platform x86_64-linux")
        c.run("docker-compose run --rm jekyll bundle lock --add-platform arm64-linux")
    print("✅ Platform support added for Linux environments")


@task
def serve(c):
    """Start Jekyll development server with live reload using Docker."""
    print("🚀 Starting Jekyll development server...")
    with c.cd(DEV_DIR):
        c.run("docker-compose up")


@task
def exec_jekyll(c, command):
    """Execute a command in the Jekyll Docker container."""
    print(f"🐚 Executing '{command}' in Jekyll container...")
    with c.cd(DEV_DIR):
        c.run(f"docker-compose run --rm jekyll {command}")


@task
def test(c):
    """Run pytest tests."""
    print("🧪 Running pytest tests...")
    c.run("poetry run pytest -v")


@task
def test_coverage(c):
    """Run pytest tests with coverage report."""
    print("🧪 Running pytest tests with coverage...")
    c.run("poetry run pytest --cov=. --cov-report=html --cov-report=term")


@task
def lint(c):
    """Run ruff linter on Python files."""
    print("🔍 Running ruff linter...")
    c.run("poetry run ruff check .")


@task
def format(c):
    """Format Python files with ruff."""
    print("✨ Formatting Python files with ruff...")
    c.run("poetry run ruff format .")


@task
def clean(c):
    """Clean up Docker containers and volumes."""
    print("🧹 Cleaning up Docker environment...")
    with c.cd(DEV_DIR):
        c.run("docker-compose down --volumes --remove-orphans")
    print("✅ Docker environment cleaned up")


@task
def dev(c):
    """Start development environment and show logs."""
    start(c)
    logs(c)
