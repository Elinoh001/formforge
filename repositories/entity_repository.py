"""Repository SQLite pour l'entité Entity (une table métier définie par
l'utilisateur au sein d'une application, ex : "Étudiant")."""

from typing import List, Optional

from core.exceptions import DatabaseError
from database.database import Database
from models.entity import Entity
from repositories.base_repository import BaseRepository


class EntityRepository(BaseRepository):
    def __init__(self, database: Optional[Database] = None):
        self._db = database or Database()

    def create(self, entity: Entity) -> Entity:
        try:
            with self._db.transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO entities
                        (id, application_id, name, slug, description, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        entity.id,
                        entity.application_id,
                        entity.name,
                        entity.slug,
                        entity.description,
                        entity.created_at,
                    ),
                )
            return entity
        except Exception as exc:
            raise DatabaseError(f"Impossible de créer l'entité : {exc}") from exc

    def get_by_id(self, entity_id: str) -> Optional[Entity]:
        row = self._db.connection.execute(
            "SELECT * FROM entities WHERE id = ?", (entity_id,)
        ).fetchone()
        return Entity.from_row(row) if row else None

    def get_by_slug(self, application_id: str, slug: str) -> Optional[Entity]:
        row = self._db.connection.execute(
            "SELECT * FROM entities WHERE application_id = ? AND slug = ?",
            (application_id, slug),
        ).fetchone()
        return Entity.from_row(row) if row else None

    def list_all(self) -> List[Entity]:
        rows = self._db.connection.execute(
            "SELECT * FROM entities ORDER BY created_at ASC"
        ).fetchall()
        return [Entity.from_row(row) for row in rows]

    def list_by_application(self, application_id: str) -> List[Entity]:
        rows = self._db.connection.execute(
            "SELECT * FROM entities WHERE application_id = ? ORDER BY created_at ASC",
            (application_id,),
        ).fetchall()
        return [Entity.from_row(row) for row in rows]

    def update(self, entity: Entity) -> Entity:
        try:
            with self._db.transaction() as conn:
                conn.execute(
                    """
                    UPDATE entities
                    SET name = ?, slug = ?, description = ?
                    WHERE id = ?
                    """,
                    (entity.name, entity.slug, entity.description, entity.id),
                )
            return entity
        except Exception as exc:
            raise DatabaseError(f"Impossible de mettre à jour l'entité : {exc}") from exc

    def delete(self, entity_id: str) -> bool:
        try:
            with self._db.transaction() as conn:
                cursor = conn.execute("DELETE FROM entities WHERE id = ?", (entity_id,))
            return cursor.rowcount > 0
        except Exception as exc:
            raise DatabaseError(f"Impossible de supprimer l'entité : {exc}") from exc

    def count_fields(self, entity_id: str) -> int:
        row = self._db.connection.execute(
            "SELECT COUNT(*) AS c FROM fields WHERE entity_id = ?", (entity_id,)
        ).fetchone()
        return row["c"]

    def count_records(self, entity_id: str) -> int:
        row = self._db.connection.execute(
            "SELECT COUNT(*) AS c FROM records WHERE entity_id = ?", (entity_id,)
        ).fetchone()
        return row["c"]
