"""Configuration centralisée du logging technique."""

import logging
import os

from core.config import LOG_PATH, ensure_storage_dirs


def setup_logging() -> None:
    """Initialise le logging vers un fichier et la console."""
    ensure_storage_dirs()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
