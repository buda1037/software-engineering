# Keycloak für Student

## Voraussetzungen

- Docker Desktop läuft.
- PostgreSQL läuft im Netzwerk `student-network`.
- Datenbank, Benutzer und Schema `keycloak` sind eingerichtet.
- Das Docker-Volume `student_keycloak_data` ist vorhanden.

## Einmalige Einrichtung

PostgreSQL muss bereits laufen. Im Hauptverzeichnis ausführen:

```powershell
docker volume create student_keycloak_data
docker compose -f extras/compose/postgres/compose.yml exec postgres psql --dbname=postgres --username=postgres
```

Passwort: `p`. In der Datenbankkonsole ausführen:

```sql
CREATE USER keycloak PASSWORD 'p';
CREATE DATABASE keycloak OWNER keycloak;
\connect keycloak
CREATE SCHEMA IF NOT EXISTS AUTHORIZATION keycloak;
ALTER ROLE keycloak SET search_path = 'keycloak';
\q
```

Diese Schritte nur bei einer neuen Einrichtung durchführen.
Keycloak legt seine Tabellen beim ersten Start automatisch an.

## Starten

Im Hauptverzeichnis des Projekts:

```powershell
docker compose -f extras/compose/keycloak/compose.yml up -d
```

Für den Betrieb mit der Anwendung startet `extras/compose/backend`
PostgreSQL und Keycloak gemeinsam, siehe README im Hauptverzeichnis.

Administrationskonsole: http://localhost:8880/admin/

Anmeldung: Benutzer `tmp`, Passwort `p`.

Der Realm `student` wird beim ersten Start aus
`realm/student-realm.json` importiert.
Ein vorhandener Realm wird nicht überschrieben.

## Testbenutzer

| Benutzer | Passwort | Rolle in student-client |
| --- | --- | --- |
| admin | p | admin |
| mamu1011 | p | student |

Diese Zugangsdaten sind für die lokale Übungsumgebung.

## Client-Geheimnis

Im Realm `student` unter:
Clients → student-client → Credentials

Das Client-Geheimnis in der `.env` im Hauptverzeichnis eintragen:

```dotenv
KEYCLOAK_CLIENT_SECRET=<Client-Geheimnis>
```

Die `.env` wird nicht eingecheckt. Keycloak erzeugt das Geheimnis;
dieser Eintrag speichert es für die lokale Verwendung.

## Stoppen

```powershell
docker compose -f extras/compose/keycloak/compose.yml down
```
