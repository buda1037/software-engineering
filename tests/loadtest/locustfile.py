"""Lasttest mit Locust für die REST-Schnittstelle."""

from pathlib import Path
from typing import Final, override

from locust import HttpUser, constant_throughput, task

CERTIFICATE: Final = (
    Path(__file__).resolve().parents[2]
    / "src/student/config/resources/tls/certificate.crt"
)


class GetUser(HttpUser):
    """Lasttest für GET-Requests als admin."""

    # 127.0.0.1 statt localhost: unter Windows verzögert localhost neue Verbindungen
    host = "https://127.0.0.1:8000"
    wait_time = constant_throughput(0.1)

    @override
    def on_start(self) -> None:
        """Einen Token anfordern und für alle Requests im Header speichern."""
        self.client.verify = str(CERTIFICATE)
        response: Final = self.client.post(
            "/auth/token",
            json={"username": "admin", "password": "p"},
        )
        token: Final[str] = response.json()["token"]
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task(100)
    def get_by_id(self) -> None:
        """GET-Requests mit einer ID als Pfadparameter."""
        for student_id in (1, 2):
            self.client.get(f"/rest/{student_id}", name="/rest/{id}")

    @task(200)
    def get_by_last_name(self) -> None:
        """GET-Requests mit einem Teil des Nachnamens als Query-Parameter."""
        for last_name in ("muster", "mann", "frau", "a"):
            self.client.get("/rest", params={"last_name": last_name})

    @task(150)
    def get_by_email(self) -> None:
        """GET-Requests mit der Emailadresse als Query-Parameter."""
        for email in ("max.mustermann@example.com", "erika.musterfrau@example.com"):
            self.client.get("/rest", params={"email": email})

    @task(50)
    def get_by_study_program(self) -> None:
        """GET-Requests mit dem Studiengang als Query-Parameter."""
        for study_program in ("WIRTSCHAFTSINFORMATIK", "DATA_SCIENCE"):
            self.client.get("/rest", params={"study_program": study_program})
