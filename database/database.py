"""Connexion SQLite et création du schéma.

Cette classe n'expose que des primitives génériques (connexion, transaction).
La logique SQL métier reste dans les repositories, ce qui permet de
remplacer SQLite par une autre source de données (API REST + PostgreSQL)
sans toucher aux couches services/screens.
"""

import logging
import sqlite3
from contextlib import contextmanager

from core.config import DATABASE_PATH, ensure_storage_dirs
from core.exceptions import DatabaseError

logger = logging.getLogger("formforge.database")


class Database:
    """Singleton d'accès à la connexion SQLite."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        ensure_storage_dirs()
        self._connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._initialized = True
        self._create_schema()

    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection

    @contextmanager
    def transaction(self):
        """Context manager transactionnel : commit si tout va bien, rollback sinon."""
        try:
            yield self._connection
            self._connection.commit()
        except Exception as exc:
            self._connection.rollback()
            logger.exception("Transaction annulée (rollback)")
            raise DatabaseError(str(exc)) from exc

    def _create_schema(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                description TEXT,
                icon TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY,
                application_id TEXT NOT NULL,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (application_id) REFERENCES applications (id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS fields (
                id TEXT PRIMARY KEY,
                entity_id TEXT NOT NULL,
                name TEXT NOT NULL,
                label TEXT NOT NULL,
                type TEXT NOT NULL,
                required INTEGER NOT NULL DEFAULT 0,
                placeholder TEXT,
                default_value TEXT,
                options_json TEXT,
                validation_json TEXT,
                position INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (entity_id) REFERENCES entities (id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS records (
                id TEXT PRIMARY KEY,
                entity_id TEXT NOT NULL,
                data_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (entity_id) REFERENCES entities (id)
                    ON DELETE CASCADE
            );
            """
        )
        self._connection.commit()
        logger.info("Schéma SQLite vérifié/initialisé (%s)", DATABASE_PATH)
