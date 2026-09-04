"""Écran Entity Builder : liste et création des entités d'une application.

Flux : ApplicationsScreen.open_application() ou
ApplicationBuilderScreen.create_application() appellent set_application()
avant de naviguer ici.
"""

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from core.constants import ScreenNames
from core.exceptions import ValidationError
from services.entity_service import EntityService
from widgets.entity_card import EntityCard

Builder.load_string(
    """
<EntityBuilderScreen>:
    canvas.before:
        Color:
            rgba: 0.07, 0.08, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(14)

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
                id: title_label
                text: ""
                bold: True
                font_size: "17sp"
                halign: "left"
                valign: "middle"
                text_size: self.size
                color: 1, 1, 1, 1
                shorten: True

        Label:
            text: "ENTITÉS"
            font_size: "13sp"
            color: 0.6, 0.62, 0.68, 1
            size_hint_y: None
            height: dp(20)
            halign: "left"
            text_size: self.size

        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: card_list
                orientation: "vertical"
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: "+  Ajouter une entité"
            size_hint_y: None
            height: dp(52)
            background_normal: ""
            background_color: 0.30, 0.45, 0.95, 1
            color: 1, 1, 1, 1
            font_size: "15sp"
            on_release: root.open_create_popup()
    """
)


class EntityBuilderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = EntityService()
        self._application = None

    def set_application(self, application):
        """Doit être appelée avant chaque navigation vers cet écran."""
        self._application = application
        self.ids.title_label.text = f"{application.icon}  {application.name.upper()}"

    def on_pre_enter(self, *args):
        if self._application is not None:
            self.refresh_list()

    def go_back(self):
        self.manager.current = ScreenNames.APPLICATIONS

    def refresh_list(self):
        container = self.ids.card_list
        container.clear_widgets()
        entities = self._service.list_entities(self._application.id)

        if not entities:
            container.add_widget(
                Label(
                    text="Aucune entité pour le moment.",
                    color=(0.6, 0.62, 0.68, 1),
                    size_hint_y=None,
                    height=dp(40),
                )
            )
            return

        for entity in entities:
            stats = self._service.get_stats(entity.id)
            card = EntityCard(
                entity_id=entity.id,
                entity_name=entity.name,
                field_count=stats["fields"],
                record_count=stats["records"],
            )
            card.bind(on_release=lambda _inst, ent=entity: self.open_entity(ent))
            container.add_widget(card)

    def open_entity(self, entity):
        """Point d'extension : ouvrira le Field Builder à l'étape suivante."""
        pass

    def open_create_popup(self):
        layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(16))

        name_input = TextInput(
            hint_text="Ex : Étudiant", multiline=False,
            size_hint_y=None, height=dp(44),
        )
        description_input = TextInput(
            hint_text="Description (optionnelle)", multiline=False,
            size_hint_y=None, height=dp(44),
        )
        error_label = Label(text="", color=(1, 0.4, 0.4, 1), size_hint_y=None, height=dp(24))

        layout.add_widget(Label(text="Nom", size_hint_y=None, height=dp(20), color=(1, 1, 1, 1)))
        layout.add_widget(name_input)
        layout.add_widget(Label(text="Description", size_hint_y=None, height=dp(20), color=(1, 1, 1, 1)))
        layout.add_widget(description_input)
        layout.add_widget(error_label)

        buttons = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(10))
        cancel_button = Button(text="Annuler")
        create_button = Button(text="Créer")
        buttons.add_widget(cancel_button)
        buttons.add_widget(create_button)
        layout.add_widget(buttons)

        popup = Popup(title="Ajouter une entité", content=layout, size_hint=(0.9, 0.55))

        def do_create(*_):
            try:
                self._service.create_entity(
                    application_id=self._application.id,
                    name=name_input.text,
                    description=description_input.text,
                )
                popup.dismiss()
                self.refresh_list()
            except ValidationError as exc:
                error_label.text = str(exc)

        create_button.bind(on_release=do_create)
        cancel_button.bind(on_release=popup.dismiss)
        popup.open()
