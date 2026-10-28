# PostgreSQL für Student

Die Einrichtung orientiert sich am Patient-Beispiel von Jürgen Zimmermann.

## Voraussetzungen

- Docker Desktop mit laufender Linux-Engine
- PowerShell
- Freier Port 5432

Vom Hauptverzeichnis des Projekts aus:

```powershell
Set-Location extras/compose/postgres
```

Die folgenden PowerShell-Befehle werden in diesem Verzeichnis ausgeführt.

## Einmalige Einrichtung

### Passwortdatei

Erstelle `password.txt` mit dem Inhalt `p`, gespeichert als UTF-8 ohne BOM.

Die Datei wird durch `.gitignore` ausgeschlossen. Die lokale
Beispielkonfiguration verwendet auch für den Datenbankbenutzer `student`
das Passwort `p`.

### Named Volumes erstellen

```powershell
docker volume create student_pg_data
docker volume create student_pg_tablespace
docker volume create student_pg_init
```

### Dateien kopieren und Berechtigungen setzen

Öffne einen Hilfscontainer:

```powershell
$studentInitPath = (Resolve-Path "./init").Path
$studentSqlPath = (Resolve-Path "../../../src/student/config/resources/postgresql").Path

docker run --rm -it --user 0 `
    --entrypoint /bin/bash `
    -v student_pg_data:/var/lib/postgresql/19/docker `
    -v student_pg_tablespace:/tablespace `
    -v student_pg_init:/init `
    -v "${studentInitPath}:/tmp/init:ro" `
    -v "${studentSqlPath}:/tmp/postgresql:ro" `
    postgres:19beta4-trixie
```

Führe in der Bash des Containers aus:

```bash
cp -r /tmp/init/. /init/
cp /tmp/postgresql/create.sql /init/student/sql/create.sql

mkdir -p /tablespace/student

chown -R postgres:postgres /init /tablespace /var/lib/postgresql/19/docker
chmod 400 /init/student/sql/* /init/student/csv/*
chmod 700 /var/lib/postgresql/19/docker /tablespace/student

ls -lR /init/student
ls -ld /tablespace/student /var/lib/postgresql/19/docker

exit
```

SQL- und CSV-Dateien gehören anschließend `postgres` und haben
Leserechte `400`. Die Datenverzeichnisse haben Rechte `700`.

### PostgreSQL starten

Zurück in PowerShell:

```powershell
docker compose up -d
docker compose ps
docker compose logs --tail 40 postgres
```

Warte, bis der Container `healthy` ist und der Server laut Log
Verbindungen annimmt.

### Datenbank, Schema und Tabellen anlegen

Führe die Befehle nacheinander aus. Das Passwort ist jeweils `p`.

```powershell
docker compose exec postgres psql --dbname=postgres --username=postgres --file=/init/student/sql/create-db.sql
docker compose exec postgres psql --dbname=student --username=student --file=/init/student/sql/create-schema.sql
docker compose exec postgres psql --dbname=student --username=student --file=/init/student/sql/create.sql
```

Diese Einrichtung wird nur einmal für die neuen Volumes durchgeführt.

### CSV-Beispieldaten laden

Öffne die Datenbankkonsole als Administrator:

```powershell
docker compose exec postgres psql --dbname=student --username=postgres
```

Passwort: `p`

Führe in `psql` aus:

```sql
SET search_path TO student;

COPY student FROM '/init/student/csv/student.csv'
    (FORMAT csv, QUOTE '"', DELIMITER ';', HEADER true);

COPY address FROM '/init/student/csv/address.csv'
    (FORMAT csv, QUOTE '"', DELIMITER ';', HEADER true);

COPY exam_result FROM '/init/student/csv/exam_result.csv'
    (FORMAT csv, QUOTE '"', DELIMITER ';', HEADER true);

\q
```

Jeder Import meldet `COPY 2`.

### Einrichtung prüfen

Öffne die Datenbankkonsole als Benutzer `student`:

```powershell
docker compose exec postgres psql --dbname=student --username=student
```

Passwort: `p`

```sql
SELECT current_schema();

\dt

SELECT
    (SELECT COUNT(*) FROM student) AS studenten,
    (SELECT COUNT(*) FROM address) AS adressen,
    (SELECT COUNT(*) FROM exam_result) AS pruefungsergebnisse;

\q
```

Erwartet werden das Schema `student`, drei Tabellen und jeweils
zwei Datensätze. Die Beispieldaten haben IDs unter 1000.
Automatisch erzeugte IDs beginnen bei 1000.

## Running the server

PostgreSQL muss zuerst laufen. Die einmalige Einrichtung steht in
[extras/compose/postgres/ReadMe.md](extras/compose/postgres/ReadMe.md).

```powershell
docker compose -f extras/compose/postgres/compose.yml up -d --wait
