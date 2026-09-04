"""Point d'entrée de l'application FormForge."""

import logging

from kivy.app import App
from kivy.uix.screenmanager import FadeTransition, ScreenManager

from core.constants import APP_NAME, ScreenNames
from database.database import Database
from screens.application_builder_screen import ApplicationBuilderScreen
from screens.applications_screen import ApplicationsScreen
from screens.entity_builder_screen import EntityBuilderScreen
from screens.home_screen import HomeScreen
from utils.logger import setup_logging

setup_logging()
logger = logging.getLogger("formforge.main")


class FormForgeApp(App):
    title = APP_NAME

    def build(self):
        try:
            Database()  # Initialise la connexion et crée le schéma si nécessaire
        except Exception:
            logger.exception("Échec de l'initialisation de la base de données")
            raise

        manager = ScreenManager(transition=FadeTransition())
        manager.add_widget(HomeScreen(name=ScreenNames.HOME))
        manager.add_widget(ApplicationsScreen(name=ScreenNames.APPLICATIONS))
        manager.add_widget(ApplicationBuilderScreen(name=ScreenNames.APPLICATION_BUILDER))
        manager.add_widget(EntityBuilderScreen(name=ScreenNames.ENTITY_BUILDER))
        manager.current = ScreenNames.HOME
        return manager


if __name__ == "__main__":
    FormForgeApp().run()
