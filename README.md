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

Die Anwendung braucht PostgreSQL und Keycloak. Die einmalige Einrichtung steht in
[extras/compose/postgres/ReadMe.md](extras/compose/postgres/ReadMe.md) und
[extras/compose/keycloak/ReadMe.md](extras/compose/keycloak/ReadMe.md),
einschließlich des Client-Geheimnisses `KEYCLOAK_CLIENT_SECRET` in `.env`.

Wähle genau eine Variante, weil beide Port 8000 verwenden.

Lokal: `extras/compose/backend` startet PostgreSQL und Keycloak, danach die
Anwendung mit uv:

```powershell
docker compose -f extras/compose/backend/compose.yml up -d --wait
uv run student
```

Falls Windows den Befehl blockiert:

```powershell
uv run --python 3.15.2 python -m student
```

Mit Docker Compose: `extras/compose/student` baut das Image und startet die
Anwendung, sobald PostgreSQL und Keycloak bereit sind:

```powershell
docker compose -f extras/compose/student/compose.yml up -d --build --wait
```

Beide Varianten verwenden das Compose-Projekt `student`.
Alle Container stoppen:

```powershell
docker compose -f extras/compose/student/compose.yml down
```

Die API ist beispielsweise unter <https://localhost:8000/rest/1> erreichbar.
Das TLS-Zertifikat ist selbstsigniert.

Die REST-Endpunkte erfordern einen Token im Header
`Authorization: Bearer <Token>`. `POST /auth/token` mit
`{"username": "admin", "password": "p"}` liefert ihn.
`GET /rest/{id}` ist für `admin` und den eigenen Studenten erlaubt,
alle anderen Endpunkte nur für `admin`.

Die GraphQL-Schnittstelle ist unter <https://localhost:8000/graphql> erreichbar,
im Browser mit GraphiQL. Die Queries `student(id)` und `students(suchparameter)`
sind wie die REST-Endpunkte geschützt. Die Mutation `create(student)` legt
einen Studenten an und ist nur für `admin` erlaubt.

In Bruno in der Umgebung `student` die geheimen Variablen `clientSecret`
(Wert aus `.env`) und `password` (`p`) setzen.

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

## Dokumentation

Die Dokumentation verwendet MkDocs mit dem Material-Theme.

Lokale Vorschau starten:

```powershell
uv run mkdocs serve --dev-addr 127.0.0.1:8001
```

Danach http://127.0.0.1:8001 öffnen.
Port 8001 ermöglicht die Vorschau neben der Student-API auf Port 8000.
Mit Strg+C beenden.

HTML-Dokumentation erzeugen:

```powershell
uv run mkdocs build
```

Die Ausgabe liegt in `site/`. Dieser Ordner wird von Git ignoriert.

## Integrationstests

Die Integrationstests senden HTTP-Anfragen an den laufenden Student-Server,
hier in Docker Compose. PostgreSQL und Keycloak müssen eingerichtet sein,
siehe [Running the server](#running-the-server).

Im Hauptverzeichnis mit PowerShell ausführen:

```powershell
docker compose -f extras/compose/student/compose.yml up -d --build --wait
$env:STUDENT_TEST_DB_PASSWORD = 'p'
uv run pytest tests/integration -v
```

Vor jedem Test wird das lokale Schema `student` gelöscht, neu angelegt
und mit den CSV-Beispieldaten geladen. Vorhandene Daten in diesem Schema
werden ersetzt. Diese Tests nur gegen die lokale Übungsdatenbank ausführen.

Der Testclient prüft das HTTPS-Zertifikat anhand der Datei
`src/student/config/resources/tls/certificate.crt`.

Nur Unit-Tests ausführen, ohne laufenden Server oder Datenbank:

```powershell
uv run pytest tests/unit
```

Die CI führt ausschließlich die Unit-Tests aus.

## Lasttest

Der Lasttest mit Locust fordert einen Token als `admin` an und sendet danach
GET-Requests mit ID und Suchparametern. Der Server muss laufen, siehe
[Running the server](#running-the-server).

```powershell
uv run locust -f tests/loadtest/locustfile.py
```

Die Weboberfläche ist unter <http://localhost:8089> erreichbar. Ohne Weboberfläche,
z.B. mit 10 Benutzern für 30 Sekunden:

```powershell
uv run locust -f tests/loadtest/locustfile.py --headless -u 10 -r 5 -t 30s
```

Für aussagekräftige Antwortzeiten in `app.toml` die mit
`locust: auskommentieren` markierten Einträge auskommentieren.
