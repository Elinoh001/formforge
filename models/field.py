"""Modèle de données pour un Field FormForge.

Un Field appartient à une Entity (ex : le champ "email" de l'entité
"Étudiant"). Il sert à la fois à générer le schéma SQLite de
l'application générée et à générer les composants de formulaire
(DynamicForm) et de liste (DynamicList).
"""

import json
import uuid
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class Field:
    """Représente un champ de données au sein d'une entité
    (ex : "email" dans l'entité "Étudiant")."""

    entity_id: str
    name: str
    label: str
    type: str = "text"
    required: bool = False
    placeholder: str = ""
    default_value: str = ""
    options: Optional[list] = None
    position: int = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_row(row) -> "Field":
        options_json = row["options_json"]
        return Field(
            id=row["id"],
            entity_id=row["entity_id"],
            name=row["name"],
            label=row["label"],
            type=row["type"],
            required=bool(row["required"]),
            placeholder=row["placeholder"] or "",
            default_value=row["default_value"] or "",
            options=json.loads(options_json) if options_json else None,
            position=row["position"] or 0,
        )