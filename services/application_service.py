"""Logique métier autour des applications : validation, génération de slug.

Les écrans Kivy ne parlent qu'à ce service, jamais directement au
repository ni à SQLite.
"""

import re
import unicodedata
from typing import List

from core.exceptions import ValidationError
from models.application import Application
from repositories.application_repository import ApplicationRepository


class ApplicationService:
    def __init__(self, repository: ApplicationRepository = None):
        self._repository = repository or ApplicationRepository()

    def create_application(
        self, name: str, description: str = "", icon: str = "📁"
    ) -> Application:
        name = (name or "").strip()
        if not name:
            raise ValidationError("Le nom de l'application est obligatoire.")
        if len(name) > 80:
            raise ValidationError("Le nom de l'application est trop long (80 caractères max).")

        slug = self._generate_unique_slug(name)
        application = Application(
            name=name,
            description=(description or "").strip(),
            icon=icon or "📁",
            slug=slug,
        )
        return self._repository.create(application)

    def list_applications(self) -> List[Application]:
        return self._repository.list_all()

    def get_application(self, application_id: str) -> Application:
        application = self._repository.get_by_id(application_id)
        if not application:
            raise ValidationError("Application introuvable.")
        return application

    def delete_application(self, application_id: str) -> bool:
        return self._repository.delete(application_id)

    def get_stats(self, application_id: str) -> dict:
        return {
            "entities": self._repository.count_entities(application_id),
            "records": self._repository.count_records(application_id),
        }

    def _generate_unique_slug(self, name: str) -> str:
        base_slug = self._slugify(name)
        slug = base_slug
        counter = 2
        while self._repository.get_by_slug(slug) is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    @staticmethod
    def _slugify(value: str) -> str:
        value = unicodedata.normalize("NFKD", value.strip().lower())
        value = value.encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-") or "application"
