"""Logique métier autour des champs (Field) : validation, type autorisé,
unicité du nom au sein d'une entité, position d'ordre."""

import re
from typing import List, Optional

from core.constants import FieldType
from core.exceptions import ValidationError
from models.field import Field
from repositories.field_repository import FieldRepository

_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class FieldService:
    def __init__(self, repository: FieldRepository = None):
        self._repository = repository or FieldRepository()

    def create_field(
        self,
        entity_id: str,
        label: str,
        field_type: str = FieldType.TEXT,
        required: bool = False,
        placeholder: str = "",
        default_value: str = "",
        options: Optional[list] = None,
        name: Optional[str] = None,
    ) -> Field:
        if not entity_id:
            raise ValidationError("Entité invalide.")

        label = (label or "").strip()
        if not label:
            raise ValidationError("Le libellé du champ est obligatoire.")
        if len(label) > 80:
            raise ValidationError("Le libellé est trop long (80 caractères max).")

        if field_type not in FieldType.ALL:
            raise ValidationError(f"Type de champ invalide : {field_type}")

        if field_type == FieldType.SELECT and not options:
            raise ValidationError("Un champ de type liste doit avoir au moins une option.")

        computed_name = name or self._slugify_name(label)
        if not _NAME_RE.match(computed_name):
            raise ValidationError(
                "Le nom technique du champ doit être en minuscules, "
                "commencer par une lettre et ne contenir que lettres/chiffres/_."
            )
        if self._repository.get_by_name(entity_id, computed_name) is not None:
            raise ValidationError(f"Un champ nommé « {computed_name} » existe déjà.")

        position = self._repository.next_position(entity_id)
        new_field = Field(
            entity_id=entity_id,
            name=computed_name,
            label=label,
            type=field_type,
            required=required,
            placeholder=(placeholder or "").strip(),
            default_value=(default_value or "").strip(),
            options=options,
            position=position,
        )
        return self._repository.create(new_field)

    def list_fields(self, entity_id: str) -> List[Field]:
        return self._repository.list_by_entity(entity_id)

    def get_field(self, field_id: str) -> Field:
        result = self._repository.get_by_id(field_id)
        if not result:
            raise ValidationError("Champ introuvable.")
        return result

    def delete_field(self, field_id: str) -> bool:
        return self._repository.delete(field_id)

    def move_up(self, entity_id: str, field_id: str) -> None:
        self._swap_position(entity_id, field_id, direction=-1)

    def move_down(self, entity_id: str, field_id: str) -> None:
        self._swap_position(entity_id, field_id, direction=1)

    def _swap_position(self, entity_id: str, field_id: str, direction: int) -> None:
        fields = self._repository.list_by_entity(entity_id)
        index = next((i for i, f in enumerate(fields) if f.id == field_id), None)
        if index is None:
            return
        target = index + direction
        if target < 0 or target >= len(fields):
            return
        current, other = fields[index], fields[target]
        current.position, other.position = other.position, current.position
        self._repository.update(current)
        self._repository.update(other)

    @staticmethod
    def _slugify_name(label: str) -> str:
        value = label.strip().lower()
        value = re.sub(r"[^a-z0-9]+", "_", value)
        value = value.strip("_") or "champ"
        if not value[0].isalpha():
            value = f"f_{value}"
        return value