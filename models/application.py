"""Modèle de données pour une Application FormForge."""

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Application:
    """Représente une application métier créée par l'utilisateur
    (ex : "Gestion des étudiants")."""

    name: str
    description: str = ""
    icon: str = "📁"
    slug: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_row(row) -> "Application":
        return Application(
            id=row["id"],
            name=row["name"],
            slug=row["slug"],
            description=row["description"] or "",
            icon=row["icon"] or "📁",
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
