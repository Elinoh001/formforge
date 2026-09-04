"""Exceptions métier personnalisées pour FormForge.

Toutes les erreurs "attendues" (validation, ressource manquante, etc.)
héritent de FormForgeError afin que les écrans puissent les intercepter
et afficher un message utilisateur clair, sans jamais faire planter
l'application.
"""


class FormForgeError(Exception):
    """Exception de base pour toutes les erreurs métier de FormForge."""


class ValidationError(FormForgeError):
    """Levée quand une donnée saisie ne respecte pas les règles métier."""


class NotFoundError(FormForgeError):
    """Levée quand une ressource demandée n'existe pas en base."""


class DatabaseError(FormForgeError):
    """Levée en cas d'erreur d'accès à la base de données."""


class DuplicateSlugError(FormForgeError):
    """Levée quand un slug existe déjà pour une ressource du même type."""
