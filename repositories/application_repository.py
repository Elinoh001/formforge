"""Repository SQLite pour l'entité Application.

Une future ApiApplicationRepository (version SaaS, FastAPI/PostgreSQL)
pourra implémenter la même interface BaseRepository sans que les services
n'aient à changer.
"""

from typing import List, Optional

from core.exceptions import DatabaseError
from database.database import Database
from models.application import Application
from repositories.base_repository import BaseRepository


class ApplicationRepository(BaseRepository):
    def __init__(self, database: Optional[Database] = None):
        self._db = database or Database()

    def create(self, application: Application) -> Application:
        try:
            with self._db.transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO applications
                        (id, name, slug, description, icon, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        application.id,
                        application.name,
                        application.slug,
                        application.description,
                        application.icon,
                        application.created_at,
                        application.updated_at,
                    ),
                )
            return application
        except Exception as exc:
            raise DatabaseError(f"Impossible de créer l'application : {exc}") from exc

    def get_by_id(self, entity_id: str) -> Optional[Application]:
        row = self._db.connection.execute(
            "SELECT * FROM applications WHERE id = ?", (entity_id,)
        ).fetchone()
        return Application.from_row(row) if row else None

    def get_by_slug(self, slug: str) -> Optional[Application]:
        row = self._db.connection.execute(
            "SELECT * FROM applications WHERE slug = ?", (slug,)
        ).fetchone()
        return Application.from_row(row) if row else None

    def list_all(self) -> List[Application]:
        rows = self._db.connection.execute(
            "SELECT * FROM applications ORDER BY updated_at DESC"
        ).fetchall()
        return [Application.from_row(row) for row in rows]

    def update(self, application: Application) -> Application:
        try:
            with self._db.transaction() as conn:
                conn.execute(
                    """
                    UPDATE applications
                    SET name = ?, slug = ?, description = ?, icon = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        application.name,
                        application.slug,
                        application.description,
                        application.icon,
                        application.updated_at,
                        application.id,
                    ),
                )
            return application
        except Exception as exc:
            raise DatabaseError(f"Impossible de mettre à jour l'application : {exc}") from exc

    def delete(self, entity_id: str) -> bool:
        try:
            with self._db.transaction() as conn:
                cursor = conn.execute(
                    "DELETE FROM applications WHERE id = ?", (entity_id,)
                )
            return cursor.rowcount > 0
        except Exception as exc:
            raise DatabaseError(f"Impossible de supprimer l'application : {exc}") from exc

    def count_entities(self, application_id: str) -> int:
        row = self._db.connection.execute(
            "SELECT COUNT(*) AS c FROM entities WHERE application_id = ?",
            (application_id,),
        ).fetchone()
        return row["c"]

    def count_records(self, application_id: str) -> int:
        row = self._db.connection.execute(
            """
            SELECT COUNT(*) AS c FROM records r
            JOIN entities e ON e.id = r.entity_id
            WHERE e.application_id = ?
            """,
            (application_id,),
        ).fetchone()
        return row["c"]
