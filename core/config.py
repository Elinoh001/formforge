"""Configuration globale : chemins et paramètres de stockage."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
DATABASE_PATH = os.path.join(STORAGE_DIR, "formforge.db")
EXPORTS_DIR = os.path.join(STORAGE_DIR, "exports")
LOG_PATH = os.path.join(STORAGE_DIR, "formforge.log")


def ensure_storage_dirs() -> None:
    """Crée les dossiers de stockage nécessaires s'ils n'existent pas encore."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(EXPORTS_DIR, exist_ok=True)
