# Trumpet Cloud Backend

The Trumpet Cloud Backend is a solid application environment designed to power the cloud backend system, primarily serving the Trumpet frontend and the listener.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Private Dependencies](#private-dependencies)
- [Local Installation](#local-installation)
  - [Environment Setup](#environment-setup)
  - [Database Setup](#database-setup)
  - [Install Dependencies](#install-dependencies)
  - [Run Project](#run-project)
- [Docker Installation](#docker-installation)
  - [Environment Setup](#environment-setup-1)
  - [Docker Compose](#docker-compose)
- [Scripts](#scripts)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Dependency Management**: Managed with [Poetry](https://python-poetry.org/) for easy handling of packages and environments.
- **Database**: Configured with PostgreSQL to manage data storage. You can connect any SQL Database you want.
- **Environment Variables**: Simplified `.env` file structure for managing sensitive and configurable parameters.
- **Containerized Setup**: Dockerized environment for easy deployment and scaling.

## Prerequisites

Ensure you have the following software installed:

- **Python 3.11+**
- **Poetry**
- **PostgreSQL** (for local setup)
- **Docker** and **Docker Compose** (for Dockerized setup)
- **Git**

## Private Dependencies

This project uses private GitHub packages for core functionality:

- `wrap-validate`
- `wrap-orm`
- `wrap-auth`
- `wrap-restify`

You'll need to configure GitHub authentication to install these dependencies.

### Creating a GitHub Personal Access Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Give it a descriptive name (e.g., "trumpet-backend-deps")
4. Select the following scopes:
   - `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't be able to see it again!)

### Local Development Setup

Configure git to use your token for private repositories:

```bash
# Option 1: Set via git config (recommended)
git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"

# Then set the environment variable
export GITHUB_TOKEN=ghp_your_token_here

# Now install dependencies
poetry install
```

Alternatively, add the export to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) to persist it:

```bash
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.bashrc
source ~/.bashrc
```

### Docker Setup

For Docker builds, pass the token as a build argument. See the [Docker Installation](#docker-installation) section.

> ⚠️ **Security Warning**: Never commit your GitHub token to version control. Always use environment variables or secure secret management.

## Local Installation

To set up the project locally, follow the steps below.

### Environment Setup

1. Copy the `env.example` file and create another file called `.env`. Modify variables if you want any changes:
   ```bash
   cp env.example .env
   ```
2. Modify `.env` file values as needed, specifically for the PostgreSQL configuration and any other secrets.

### Database Setup

1. Ensure PostgreSQL is installed and running locally.
2. Create a PostgreSQL database for the project:
   ```bash
   psql -U postgres -c "CREATE DATABASE <your-db-name>;"
   ```
3. Update the `.env` file with your PostgreSQL credentials, including `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, and `DB_PASSWORD`.

### Install Dependencies

1. Ensure you have [configured GitHub authentication](#private-dependencies) for private packages.

2. Use Poetry to install project dependencies:
   ```bash
   poetry install --no-root --no-dev
   ```

3. Activate the Poetry environment:
   ```bash
   poetry shell
   ```

### Run Project

To start the project locally, run the `entrypoint.sh` script:

```bash
./entrypoint.sh
```

## Docker Installation

For a Dockerized setup, follow the instructions below.

### Environment Setup

1. Copy the `env.example` or `.env.example.arm` file to `.env`:
   ```bash
   # For Linux or Windows OS
   cp env.example .env

   # For Mac OS
   cp env.example.arm .env
   ```

2. Add your `frontend` host into `.env` file in `ALLOWED_HOSTS` variables with comma separated value.

3. Forward / Map your `WEB-LISTENER` host using `ngrok`. Run:
   ```bash
   ngrok http <web-listener host>
   ```

4. Copy the forwarding URL and update the `LISTENER_WEBHOOK_URL` variable in `.env` file as `<LISTENER_WEBHOOK_URL>/listen`.

5. Add your GitHub token to the `.env` file:
   ```bash
   GITHUB_TOKEN=ghp_your_token_here
   ```

6. Update any other environment variables in `.env` as needed.

### Docker Compose

To start the project in a Docker environment:

```bash
# For Linux or Windows OS
docker compose -f docker-compose.yml up --build -d

# For Mac OS
docker compose -f docker-compose.yml.arm up --build -d
```

This command will:

- Build Docker images as per the configurations in `docker-compose.yml`.
- Start the services as per the defined configuration.
- Change the configuration of the `docker-compose.yml` as per your need.

> **Note**: The `GITHUB_TOKEN` from your `.env` file is used during the build process to authenticate with GitHub for private dependencies. Ensure this token is kept secure and never committed to version control.

### Additional Docker Commands

- To stop the Docker containers:
  ```bash
  docker compose down
  ```

- To rebuild without cache:
  ```bash
  docker compose build --no-cache
  ```

- To view logs:
  ```bash
  docker compose logs -f
  ```

## Scripts

- **entrypoint.sh**: Initializes the project with any necessary startup scripts and configurations.

## Project Structure

```plaintext
.
├── adapters/           
├── application_layer/                   
├── domain_layer/           # Domain logics
├── main.py 
├── app_layer_entrypoint.py  
├── pyproject.toml          # Poetry dependencies
└── README.md               # Project README
```

## Documentation

- [Logic Layer Guide](domain_layer/logics/readme/readme.md) - Comprehensive guide for the domain logic layer architecture and implementation.

## Contributing

We welcome contributions from the community! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting a Pull Request.

Quick steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For more details on coding standards, commit conventions, and the review process, see [CONTRIBUTING.md](CONTRIBUTING.md).
