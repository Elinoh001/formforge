"""Charge un schéma de projet complet à partir des données réelles
stockées en SQLite par FormForge (Application, Entities, Fields).

RÈGLE : ce module ne doit JAMAIS contenir de logique conditionnelle sur
le nom d'une application ou d'une entité précise (interdit par les
règles de développement de FormForge). Il transforme n'importe quel
projet en un schéma générique consommé par le générateur.
"""

import re
import unicodedata
from dataclasses import dataclass, field
from typing import List

from core.exceptions import ValidationError
from services.application_service import ApplicationService
from services.entity_service import EntityService
from services.field_service import FieldService

# Mapping des types de champs FormForge vers les types de colonnes SQLite
# de l'application GÉNÉRÉE (indépendante de FormForge).
SQLITE_TYPE_MAP = {
    "text": "TEXT",
    "textarea": "TEXT",
    "number": "REAL",
    "email": "TEXT",
    "select": "TEXT",
    "boolean": "INTEGER",
    "date": "TEXT",
}

# Mapping des types de champs FormForge vers le composant Kivy utilisé
# pour générer un formulaire dynamique dans l'application GÉNÉRÉE.
WIDGET_TYPE_MAP = {
    "text": "text_input",
    "textarea": "text_input_multiline",
    "number": "number_input",
    "email": "text_input",
    "select": "spinner",
    "boolean": "checkbox",
    "date": "text_input",
}


@dataclass
class FieldSchema:
    name: str
    label: str
    type: str
    required: bool
    default_value: str
    options: list
    sqlite_type: str
    widget_type: str


@dataclass
class EntitySchema:
    name: str
    slug: str
    class_name: str
    fields: List[FieldSchema] = field(default_factory=list)


@dataclass
class ProjectSchema:
    name: str
    slug: str
    package_name: str
    version: str
    icon: str
    class_name: str
    entities: List[EntitySchema] = field(default_factory=list)


def _pascal_case(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    parts = re.split(r"[^a-zA-Z0-9]+", value)
    return "".join(p.capitalize() for p in parts if p) or "Item"


def load_project_schema(application_id: str) -> ProjectSchema:
    """Construit le schéma complet d'un projet à partir de son id.

    Lève ValidationError si l'application n'existe pas ou si elle ne
    contient aucune entité (rien de significatif à générer).
    """
    application_service = ApplicationService()
    entity_service = EntityService()
    field_service = FieldService()

    application = application_service.get_application(application_id)
    entities = entity_service.list_entities(application.id)

    if not entities:
        raise ValidationError(
            "Impossible de générer le projet : ajoutez au moins une entité "
            "(ex : « Étudiant ») avant de générer."
        )

    entity_schemas: List[EntitySchema] = []
    for entity in entities:
        db_fields = field_service.list_fields(entity.id)
        if not db_fields:
            raise ValidationError(
                f"L'entité « {entity.name} » n'a aucun champ. "
                "Ajoutez au moins un champ avant de générer."
            )

        field_schemas = [
            FieldSchema(
                name=f.name,
                label=f.label,
                type=f.type,
                required=f.required,
                default_value=f.default_value,
                options=f.options or [],
                sqlite_type=SQLITE_TYPE_MAP.get(f.type, "TEXT"),
                widget_type=WIDGET_TYPE_MAP.get(f.type, "text_input"),
            )
            for f in db_fields
        ]

        entity_schemas.append(
            EntitySchema(
                name=entity.name,
                slug=entity.slug.replace("-", "_"),
                class_name=_pascal_case(entity.name),
                fields=field_schemas,
            )
        )

    return ProjectSchema(
        name=application.name,
        slug=application.slug.replace("-", "_"),
        package_name=f"org.formforge.{application.slug.replace('-', '')}",
        version="1.0.0",
        icon=application.icon,
        class_name=_pascal_case(application.name),
        entities=entity_schemas,
    )