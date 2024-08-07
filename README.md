# Trumpet Researcher Server

Trumpet Researcher Server is a project focused on privacy-preserving federated learning. Python is the
primary programming language used in this project.

## Table of Contents

- [Installation](#installation)
- [Local Installation](#local-installation)
- [Production Deployment](#production-deployment)
- [Tools](#tools)
- [Git Branching Strategies](#git-branching-strategies)
- [Git Commit Guidelines](#git-commit-guidelines)
- [Folder Structure](#folder-structure)

## Installation

### Local Installation

To set up the Trumpet Cloud project locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone git@github.com:tvs-enterprise/TrumpetResearcherServer.git
    cd src
    ```

2. **Install Poetry:**
   Follow the installation instructions from the [Poetry website](https://python-poetry.org/docs/#installation).

3. **Install dependencies:**
    ```bash
    poetry install
    ```

### Production Deployment

For production deployment, we use Docker and Kubernetes.

1. **Docker Compose:**
    - Ensure Docker and Docker Compose are installed on your machine.
    - We provide a `docker-compose.yml` file for setting up the application along with PostgreSQL. To deploy using
      Docker Compose, run:
      ```bash
      docker-compose up --build
      ```

2. **Kubernetes:**
    - Ensure you have a Kubernetes cluster and `kubectl` installed and configured.
    - We provide Kubernetes configuration files in the `k8s` directory.
    - To deploy the application, run:
      ```bash
      kubectl apply -f k8s/
      ```

    - This will create the necessary Kubernetes resources (deployments, services, etc.) to run the application.

## Tools

- **API Documentation:**
    - The API documentation is available in both ReDoc and Swagger formats.
    - Swagger: 
    - ReDoc: 

## Git Branching Strategies

We use the **Gitflow** branching strategy to manage our project development. The main branches are:

- `main`: The production-ready branch.
- `stage`: Branch with stable codes merged from develop branch where QA will be done
- `develop`: The branch where features are integrated before being released.

Feature branches, release branches, and hotfix branches are created from `develop` and `main` as needed.

## Git Commit Guidelines

We follow the **Conventional Commit** guidelines for our commit messages to ensure a consistent and informative history.
Each commit message consists of a type, an optional scope, and a subject.

## Folder Structure

The project structure is organized as follows: