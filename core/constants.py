"""Constantes globales de FormForge."""

APP_NAME = "FormForge"
APP_VERSION = "0.1.0"


class ScreenNames:
    """Noms des écrans utilisés par le ScreenManager."""

    SPLASH = "splash"
    HOME = "home"
    APPLICATIONS = "applications"
    APPLICATION_BUILDER = "application_builder"
    ENTITY_BUILDER = "entity_builder"
    FIELD_BUILDER = "field_builder"
    PREVIEW = "preview"
    RECORDS = "records"
    FORM = "form"
    SETTINGS = "settings"


class FieldType:
    """Types de champs supportés par le MVP."""

    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    EMAIL = "email"
    SELECT = "select"
    BOOLEAN = "boolean"
    DATE = "date"

    ALL = [TEXT, TEXTAREA, NUMBER, EMAIL, SELECT, BOOLEAN, DATE]


DEFAULT_ICON = "📁"
