"""Écran de création d'une application.

Remplace la popup utilisée à l'étape 1 : conforme au flux Accueil →
Mes applications → Créer une application → Créer une entité.
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from core.constants import ScreenNames
from core.exceptions import ValidationError
from services.application_service import ApplicationService

Builder.load_string(
    """
<ApplicationBuilderScreen>:
    canvas.before:
        Color:
            rgba: 0.07, 0.08, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            Button:
                text: "←"
                size_hint_x: None
                width: dp(44)
                background_normal: ""
                background_color: 0, 0, 0, 0
                color: 1, 1, 1, 1
                on_release: root.go_back()
            Label:
                text: "CRÉER UNE APPLICATION"
                bold: True
                font_size: "16sp"
                halign: "left"
                valign: "middle"
                text_size: self.size
                color: 1, 1, 1, 1

        Label:
            text: "Nom"
            size_hint_y: None
            height: dp(20)
            halign: "left"
            text_size: self.size
            color: 0.75, 0.77, 0.82, 1
        TextInput:
            id: name_input
            hint_text: "Ex : Gestion des étudiants"
            multiline: False
            size_hint_y: None
            height: dp(46)

        Label:
            text: "Description"
            size_hint_y: None
            height: dp(20)
            halign: "left"
            text_size: self.size
            color: 0.75, 0.77, 0.82, 1
        TextInput:
            id: description_input
            hint_text: "Ex : Application de gestion académique"
            multiline: False
            size_hint_y: None
            height: dp(46)

        Label:
            text: "Icône (emoji)"
            size_hint_y: None
            height: dp(20)
            halign: "left"
            text_size: self.size
            color: 0.75, 0.77, 0.82, 1
        TextInput:
            id: icon_input
            text: "📁"
            multiline: False
            size_hint_y: None
            height: dp(46)

        Label:
            id: error_label
            text: ""
            color: 1, 0.4, 0.4, 1
            size_hint_y: None
            height: dp(22)

        Widget:

        Button:
            text: "Créer"
            size_hint_y: None
            height: dp(52)
            background_normal: ""
            background_color: 0.30, 0.45, 0.95, 1
            color: 1, 1, 1, 1
            font_size: "15sp"
            on_release: root.create_application()
    """
)


class ApplicationBuilderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = ApplicationService()

    def on_pre_enter(self, *args):
        self.ids.name_input.text = ""
        self.ids.description_input.text = ""
        self.ids.icon_input.text = "📁"
        self.ids.error_label.text = ""

    def go_back(self):
        self.manager.current = ScreenNames.APPLICATIONS

    def create_application(self):
        try:
            application = self._service.create_application(
                name=self.ids.name_input.text,
                description=self.ids.description_input.text,
                icon=self.ids.icon_input.text or "📁",
            )
        except ValidationError as exc:
            self.ids.error_label.text = str(exc)
            return

        # Flux imposé : après création, on enchaîne directement sur
        # la création d'entités pour cette nouvelle application.
        entity_builder = self.manager.get_screen(ScreenNames.ENTITY_BUILDER)
        entity_builder.set_application(application)
        self.manager.current = ScreenNames.ENTITY_BUILDER
