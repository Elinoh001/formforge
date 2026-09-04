"""Modèle de données pour une Entity FormForge."""

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Entity:
    """Représente une entité métier au sein d'une application
    (ex : "Étudiant" dans l'application "Gestion des étudiants")."""

    application_id: str
    name: str
    description: str = ""
    slug: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_row(row) -> "Entity":
        return Entity(
            id=row["id"],
            application_id=row["application_id"],
            name=row["name"],
            slug=row["slug"],
            description=row["description"] or "",
            created_at=row["created_at"],
        )
