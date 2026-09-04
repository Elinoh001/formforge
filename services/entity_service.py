"""Logique métier autour des entités : validation, slug unique par application.

Le slug d'une entité n'a besoin d'être unique qu'à l'intérieur de son
application (deux applications différentes peuvent chacune avoir une
entité "client").
"""

import re
import unicodedata
from typing import List

from core.exceptions import ValidationError
from models.entity import Entity
from repositories.entity_repository import EntityRepository


class EntityService:
    def __init__(self, repository: EntityRepository = None):
        self._repository = repository or EntityRepository()

    def create_entity(self, application_id: str, name: str, description: str = "") -> Entity:
        name = (name or "").strip()
        if not application_id:
            raise ValidationError("Application invalide.")
        if not name:
            raise ValidationError("Le nom de l'entité est obligatoire.")
        if len(name) > 80:
            raise ValidationError("Le nom de l'entité est trop long (80 caractères max).")

        slug = self._generate_unique_slug(application_id, name)
        entity = Entity(
            application_id=application_id,
            name=name,
            description=(description or "").strip(),
            slug=slug,
        )
        return self._repository.create(entity)

    def list_entities(self, application_id: str) -> List[Entity]:
        return self._repository.list_by_application(application_id)

    def get_entity(self, entity_id: str) -> Entity:
        entity = self._repository.get_by_id(entity_id)
        if not entity:
            raise ValidationError("Entité introuvable.")
        return entity

    def delete_entity(self, entity_id: str) -> bool:
        return self._repository.delete(entity_id)

    def get_stats(self, entity_id: str) -> dict:
        return {
            "fields": self._repository.count_fields(entity_id),
            "records": self._repository.count_records(entity_id),
        }

    def _generate_unique_slug(self, application_id: str, name: str) -> str:
        base_slug = self._slugify(name)
        slug = base_slug
        counter = 2
        while self._repository.get_by_slug(application_id, slug) is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    @staticmethod
    def _slugify(value: str) -> str:
        value = unicodedata.normalize("NFKD", value.strip().lower())
        value = value.encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-") or "entite"
