# Software Engineering

Results of the Software Engineering module at [Hochschule Karlsruhe (HKA)](https://www.h-ka.de).

## Requirements

- [Python 3.15](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.12.20 or later
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- For SonarQube and OWASP Dependency Check: the course tools in `C:\Zimmermann` must be installed and configured properly

## Setup

Create the virtual environment and install all dependencies including the development tools:

```powershell
uv sync
```

## Running the server

Locally:

```powershell
uv run student
```

With Docker Compose (builds the image):

```powershell
docker compose up
```

URL: <https://127.0.0.1:8000>, e.g. <https://127.0.0.1:8000/hello>. The TLS certificate is self-signed.

## Checks and tests

Commands run by the CI:

```powershell
uv run ruff check src tests
uv run ruff format --check src tests
uv run ty check
uv run pyrefly check
uv run yamllint --strict .
uv run pytest
uv audit
```

`uv audit` checks the locked dependencies for known vulnerabilities.

## Library Skills

[Library Skills](https://github.com/tiangolo/library-skills) provides the agent skills shipped with FastAPI in `.agents/skills` and `.claude/skills`. Both directories are excluded from Git. Create them after `uv sync`:

```powershell
uvx library-skills --all --claude --copy --yes
```

`--copy` avoids symlinks, which require Developer Mode on Windows. After a FastAPI update, delete both directories and run the command again.

## Code analysis with SonarQube

Start the server:

```powershell
docker compose -f extras/compose/sonarqube/compose.yml up -d
```

Plugins are loaded from `C:\Zimmermann\volumes\sonarqube\extensions`.

Initial setup:

1. Open <http://localhost:9000>, log in as `admin` / `admin` and change the password.
2. Generate a _Global Analysis Token_ under _My Account > Security_.
3. Set the token as `SONAR_TOKEN` in `.env` (template: `.env.example`).

Then run the analysis:

```powershell
uv run sonar-scanner.py
```

Results: <http://localhost:9000/dashboard?id=student>

Stop the server:

```powershell
docker compose -f extras/compose/sonarqube/compose.yml down
```

## OWASP Dependency Check

Requires an [NVD API key](https://nvd.nist.gov/developers/request-an-api-key) as `NVD_API_KEY` in `.env` (template: `.env.example`).

```powershell
uv run extras/dependency-check.py
```

Report: `dependency-check-report.html`. The first run downloads the NVD database (about two hours). False positives are suppressed with a justification in [extras/suppression.xml](extras/suppression.xml).
