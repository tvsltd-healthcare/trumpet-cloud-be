# Backend Playground (BE Playground)

Backend Playground is a robust backend application environment tailored for development, testing, and experimenting with
backend configurations, database setups, and integrations.  

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Local Installation](#local-installation)
    - [Environment Setup](#environment-setup)
    - [Database Setup](#database-setup)
    - [Install Dependencies](#install-dependencies)
    - [Run Project](#run-project)
- [Docker Installation](#docker-installation)
    - [Environment Setup](#environment-setup)
    - [Docker Compose](#docker-compose)
- [Scripts](#scripts)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Dependency Management**: Managed with [Poetry](https://python-poetry.org/) for easy handling of packages and
  environments.
- **Database**: Configured with PostgreSQL to manage data storage. You can connect any SQL Database you want.
- **Environment Variables**: Simplified `.env` file structure for managing sensitive and configurable parameters.
- **Containerized Setup**: Dockerized environment for easy deployment and scaling.

## Prerequisites

Ensure you have the following software installed:

- **Python 3.11+**
- **Poetry**
- **PostgreSQL** (for local setup)
- **Docker** and **Docker Compose** (for Dockerized setup)

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
   psql -U postgres -c "CREATE DATABASE <you-db-name>;"
   ```
3. Update the `.env` file with your PostgreSQL credentials, including `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, and
   `DB_PASSWORD`.

### Install Dependencies

1. Use Poetry to install project dependencies:
   ```bash
   poetry install --no-root --no-dev
   ```
2. Activate the Poetry environment:
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

1. Copy the `env.example` or `.env.example.arm`  file to `.env`:
```bash
   # For Linux or Windows OS
   cp env.example .env

   # For Mac OS
   cp env.example.arm .env
```
2. Add your `frontend` host into `.env` file in `ALLOWED_HOSTS` variables with comma separated value.
3. Forwording / Mapping your `WEB-LISTENER` host using `ngrok`. Run:
   ```bash
      ngrok http <web-listener host>
   ```

4. Copy the forwording Url  and Update the `LISTENER_WEBHOOK_URL` variables in `.env` file  as like as `<LISTENER_WEBHOOK_URL>/listen`. 
4. Update any environment variables in `.env` as needed.

### Docker Compose

To start the project in a Docker environment:

```bash
   # For Linux or Windows Os
   docker compose -f docker-compose.yml up —build -d

   # For Mac Os
   docker compose -f docker-compose.yml.arm up —build -d
```

This command will:

- Build Docker images as per the configurations in `docker-compose.yml`.
- Start the services as per the defined configuration.
- Change the configuration of the `docker-compose.yml` as per your need. 

### Additional Docker Commands

- To stop the Docker containers:
  ```bash
  docker compose down
  ```

## Scripts

- **entrypoint.sh**: Initializes the project with any necessary startup scripts and configurations.

## Project Structure

```plaintext
.
├── src/
```

## Contributing

If you want to contribute, please fork the repository, create a new branch, make your changes, and open a pull request.
