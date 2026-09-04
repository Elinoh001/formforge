"""Repository SQLite pour l'entité Field (un champ de données d'une
Entity, ex : "email" dans "Étudiant")."""

import json
from typing import List, Optional

from core.exceptions import DatabaseError
from database.database import Database
from models.field import Field
from repositories.base_repository import BaseRepository


class FieldRepository(BaseRepository):
    def __init__(self, database: Optional[Database] = None):
        self._db = database or Database()

    def create(self, field: Field) -> Field:
        try:
            with self._db.transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO fields
                        (id, entity_id, name, label, type, required,
                         placeholder, default_value, options_json,
                         validation_json, position)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        field.id,
                        field.entity_id,
                        field.name,
                        field.label,
                        field.type,
                        int(field.required),
                        field.placeholder,
                        field.default_value,
                        json.dumps(field.options) if field.options else None,
                        None,
                        field.position,
                    ),
                )
            return field
        except Exception as exc:
            raise DatabaseError(f"Impossible de créer le champ : {exc}") from exc

    def get_by_id(self, entity_id: str) -> Optional[Field]:
        row = self._db.connection.execute(
            "SELECT * FROM fields WHERE id = ?", (entity_id,)
        ).fetchone()
        return Field.from_row(row) if row else None

    def get_by_name(self, entity_id: str, name: str) -> Optional[Field]:
        row = self._db.connection.execute(
            "SELECT * FROM fields WHERE entity_id = ? AND name = ?",
            (entity_id, name),
        ).fetchone()
        return Field.from_row(row) if row else None

    def list_all(self) -> List[Field]:
        rows = self._db.connection.execute(
            "SELECT * FROM fields ORDER BY position ASC"
        ).fetchall()
        return [Field.from_row(row) for row in rows]

    def list_by_entity(self, entity_id: str) -> List[Field]:
        rows = self._db.connection.execute(
            "SELECT * FROM fields WHERE entity_id = ? ORDER BY position ASC",
            (entity_id,),
        ).fetchall()
        return [Field.from_row(row) for row in rows]

    def update(self, field: Field) -> Field:
        try:
            with self._db.transaction() as conn:
                conn.execute(
                    """
                    UPDATE fields
                    SET name = ?, label = ?, type = ?, required = ?,
                        placeholder = ?, default_value = ?, options_json = ?,
                        position = ?
                    WHERE id = ?
                    """,
                    (
                        field.name,
                        field.label,
                        field.type,
                        int(field.required),
                        field.placeholder,
                        field.default_value,
                        json.dumps(field.options) if field.options else None,
                        field.position,
                        field.id,
                    ),
                )
            return field
        except Exception as exc:
            raise DatabaseError(f"Impossible de mettre à jour le champ : {exc}") from exc

    def delete(self, entity_id: str) -> bool:
        try:
            with self._db.transaction() as conn:
                cursor = conn.execute("DELETE FROM fields WHERE id = ?", (entity_id,))
            return cursor.rowcount > 0
        except Exception as exc:
            raise DatabaseError(f"Impossible de supprimer le champ : {exc}") from exc

    def next_position(self, entity_id: str) -> int:
        row = self._db.connection.execute(
            "SELECT MAX(position) AS m FROM fields WHERE entity_id = ?",
            (entity_id,),
        ).fetchone()
        return (row["m"] + 1) if row["m"] is not None else 0