## [1.0.0] - 2026-10-30

### 🚀 Features

- Store students with address and exam results in PostgreSQL
- Read students by ID and search them via REST
- Create, update and delete students via REST
- Protect the REST endpoints with roles in Keycloak
- Query and create students via GraphQL
- Run the application with PostgreSQL and Keycloak in Docker Compose
- Configure logging with loguru

### 🐛 Bug Fixes

- Connect the student container to the PostgreSQL network
- Let Keycloak generate the client secret
- Preserve environment URLs in Bruno error requests

### 📚 Documentation

- Document the domain and data model with MkDocs
- Document the setup of PostgreSQL and Keycloak
- Write the README and docstrings in German

### 🚜 Refactor

- Use English names for the search parameters and address DTO

### 🧪 Testing

- Add integration tests for the REST and GraphQL endpoints
- Add Bruno requests for all endpoints
- Add load tests with Locust

### ⚙️ Miscellaneous Tasks

- Check the code with Ruff, ty, Pyrefly and yamllint in the CI
- Check dependencies with uv audit and OWASP Dependency Check
- Analyze the code with SonarQube
- Set up Library Skills

## [0.2.0] - 2026-10-20

### 🚀 Features

- *(hello-world)* [**breaking**] Remove hello-world package
- *(student)* Add student package
- Serve student REST API over HTTPS
- Run server with Docker Compose

### 🐛 Bug Fixes

- Fix invalid linter config

### 🎨 Styling

- Normalize line endings to LF

### ⚙️ Miscellaneous Tasks

- Add FastAPI
- Add Uvicorn
- Add httpx2
- Configure VS Code workspace settings

## [0.1.0] - 2026-10-12

### 🚀 Features

- Add hello-world package

### 📚 Documentation

- Add README.md

### ⚙️ Miscellaneous Tasks

- Add LICENSE
- Add AUTHORS
- Add .editorconfig
- Initialize uv Python project
- Add pytest
- Add ty
- Add Pyrefly
- Add Ruff
- Add yamllint
- Add git-cliff

### 💼 Other

- Add Dockerfile and compose.yml
