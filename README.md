# Software Engineering

Ergebnisse des Moduls Software Engineering an der
[Hochschule Karlsruhe (HKA)](https://www.h-ka.de): eine Anwendung zur Verwaltung
von Studenten mit REST- und GraphQL-Schnittstelle.

## Voraussetzungen

- [Python 3.15](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.12.20 oder neuer
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Für SonarQube und OWASP Dependency Check: die Kurswerkzeuge in `C:\Zimmermann`,
  installiert und eingerichtet

## Einrichtung

Virtuelle Umgebung mit allen Abhängigkeiten einschließlich der Entwicklungswerkzeuge
anlegen:

```powershell
uv sync
```

Die Datei `.env` aus `.env.example` anlegen. Sie wird von Git ignoriert.

PostgreSQL und Keycloak einmalig einrichten, wie in
[extras/compose/postgres/ReadMe.md](extras/compose/postgres/ReadMe.md) und
[extras/compose/keycloak/ReadMe.md](extras/compose/keycloak/ReadMe.md) beschrieben,
einschließlich des Client-Geheimnisses `KEYCLOAK_CLIENT_SECRET` in `.env`.

## Server starten

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

## Schnittstellen

Die REST-Schnittstelle ist beispielsweise unter <https://localhost:8000/rest/1>
erreichbar. Das TLS-Zertifikat ist selbstsigniert.

Die REST-Endpunkte erfordern einen Token im Header
`Authorization: Bearer <Token>`. `POST /auth/token` mit
`{"username": "admin", "password": "p"}` liefert ihn.
`GET /rest/{id}` ist für `admin` und den eigenen Studenten erlaubt,
alle anderen Endpunkte nur für `admin`.

Die GraphQL-Schnittstelle ist unter <https://localhost:8000/graphql> erreichbar,
im Browser mit GraphiQL. Die Queries `student(id)` und `students(searchParameters)`
sind wie die REST-Endpunkte geschützt. Die Mutation `create(student)` legt
einen Studenten an und ist nur für `admin` erlaubt.

Die Bruno-Collection liegt in `extras/bruno/student`. In der Umgebung `student`
die geheimen Variablen `clientSecret` (Wert aus `.env`) und `password` (`p`) setzen.

## Prüfungen und Tests

Befehle der CI:

```powershell
uv run ruff check src tests
uv run ruff format --check src tests
uv run ty check
uv run pyrefly check
uv run yamllint --strict .
uv run pytest tests/unit
uv audit
```

`uv audit` prüft die gesperrten Abhängigkeiten auf bekannte Schwachstellen.

### Unit-Tests

Die Unit-Tests brauchen keinen laufenden Server und keine Datenbank:

```powershell
uv run pytest tests/unit
```

### Integrationstests

Die Integrationstests senden HTTP-Anfragen an den laufenden Server, hier in
Docker Compose. Im Hauptverzeichnis mit PowerShell ausführen:

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

### Lasttest

Der Lasttest mit Locust fordert einen Token als `admin` an und sendet danach
GET-Requests mit ID und Suchparametern. Der Server muss laufen.

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

## Dokumentation

Die Dokumentation verwendet MkDocs mit dem Material-Theme.

Lokale Vorschau starten:

```powershell
uv run mkdocs serve --dev-addr 127.0.0.1:8001
```

Danach <http://127.0.0.1:8001> öffnen.
Port 8001 ermöglicht die Vorschau neben dem Server auf Port 8000.
Mit Strg+C beenden.

HTML-Dokumentation erzeugen:

```powershell
uv run mkdocs build
```

Die Ausgabe liegt in `site/`. Dieser Ordner wird von Git ignoriert.

## Code-Analyse mit SonarQube

Server starten:

```powershell
docker compose -f extras/compose/sonarqube/compose.yml up -d
```

Die Plugins werden aus `C:\Zimmermann\volumes\sonarqube\extensions` geladen.

Einmalige Einrichtung:

1. <http://localhost:9000> öffnen, als `admin` / `admin` anmelden und das Passwort ändern.
2. Unter _My Account > Security_ einen _Global Analysis Token_ erzeugen.
3. Den Token als `SONAR_TOKEN` in `.env` eintragen.

Danach die Analyse starten:

```powershell
uv run sonar-scanner.py
```

Ergebnisse: <http://localhost:9000/dashboard?id=student>

Server stoppen:

```powershell
docker compose -f extras/compose/sonarqube/compose.yml down
```

## OWASP Dependency Check

Erfordert einen [NVD API Key](https://nvd.nist.gov/developers/request-an-api-key)
als `NVD_API_KEY` in `.env`.

```powershell
uv run extras/dependency-check.py
```

Bericht: `dependency-check-report.html`. Der erste Lauf lädt die NVD-Datenbank
herunter (etwa zwei Stunden). Fehlalarme sind mit Begründung in
[extras/suppression.xml](extras/suppression.xml) unterdrückt.

## Library Skills

[Library Skills](https://github.com/tiangolo/library-skills) stellt die mit
FastAPI ausgelieferten Agent Skills in `.agents/skills` und `.claude/skills`
bereit. Beide Verzeichnisse werden von Git ignoriert. Nach `uv sync` anlegen:

```powershell
uvx library-skills --all --claude --copy --yes
```

`--copy` vermeidet symbolische Links, die unter Windows den Entwicklermodus
erfordern. Nach einem Update von FastAPI beide Verzeichnisse löschen und den
Befehl erneut ausführen.
