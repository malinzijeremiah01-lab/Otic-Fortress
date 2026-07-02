# Fortress Backend

The Fortress Backend is the Node.js and Express.js service layer for the Otic Fortress AI Cybersecurity Platform. It is responsible for backend APIs, platform orchestration, security-focused business logic, and future integrations with Microsoft Azure services such as Azure SQL, Azure Cosmos DB, Azure Key Vault, and Application Insights.

## Project Structure

```text
BACKEND/
|-- src/
|-- package.json
|-- package-lock.json
|-- .env.example
|-- .gitignore
`-- README.md
```

- `src/`: Application source code, routes, services, middleware, and backend modules.
- `package.json`: Node.js project metadata, scripts, and dependency definitions.
- `package-lock.json`: Locked dependency versions for repeatable installs.
- `.env.example`: Example environment configuration using placeholder values only.
- `.gitignore`: Backend-specific files and folders excluded from version control.
- `README.md`: Developer documentation for the backend service.

## Architecture Overview

The Fortress Backend exposes REST APIs that communicate with the platform's security engine and cloud services.

High-level flow:

Developer
↓
GitHub Repository
↓
GitHub Actions
↓
Backend Service
↓
Azure SQL / Cosmos DB
↓
Azure Key Vault
↓
Azure Monitor & Application Insights

## Prerequisites

- Node.js 20+
- npm
- Git
- VS Code (recommended)

## Installation

```bash
git clone <repository>
cd BACKEND
npm install
```

## Environment Configuration

Copy `.env.example` to `.env` before running the backend locally:

```bash
cp .env.example .env
```

Configure all required environment variables in `.env` for your local environment. Never commit `.env` or any file containing real secrets, credentials, connection strings, tokens, or private keys.

## Running the Application

Start the application in standard runtime mode:

```bash
npm start
```

Start the application in development mode:

```bash
npm run dev
```

`npm start` is intended for normal application startup. `npm run dev` is intended for local development workflows, typically with automatic reloads, debugging, or developer-focused tooling when configured.

## Running Tests

```bash
npm test
```

All tests should pass before opening a Pull Request.

## CI/CD

GitHub Actions automatically:

- Installs dependencies
- Runs tests
- Runs linting
- Verifies the project

All CI checks must pass before merging changes into protected branches.

## Coding Standards

- Follow the project architecture.
- Use meaningful commit messages.
- Write clean, maintainable code.
- Update documentation when behavior, configuration, or workflows change.
- Never commit secrets, credentials, tokens, private keys, or production configuration values.

## Security

Secrets belong in Azure Key Vault and should be accessed through approved application configuration patterns. Environment variables must remain private and should only contain local or deployment-specific values. Dependencies should be reviewed and updated regularly to reduce security and supply chain risk.

## API Versioning

All backend endpoints follow versioned routing.

Example:

/api/v1/auth

/api/v1/users

/api/v1/alerts

Future versions will use:

/api/v2/

## Branching Strategy

main
Production-ready code.

develop
Integration branch.

feature/*
Individual developer work.

bugfix/*
Bug fixes.

hotfix/*
Production fixes.

## Future Integrations

Planned platform integrations include:

- Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Azure SQL
- Azure Cosmos DB
- Azure Monitor
- Application Insights
- Azure Key Vault

## Contributing

1. Create a feature branch.
2. Make changes.
3. Commit your work.
4. Push the branch.
5. Open a Pull Request.
6. Wait for code review.
7. Merge after approval and passing CI checks.

## License

This project follows the repository's licensing terms.
