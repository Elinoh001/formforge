"""Écran « Mes applications » : liste des applications créées et point
d'entrée vers l'Application Builder et l'Entity Builder."""

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from core.constants import ScreenNames
from services.application_service import ApplicationService
from widgets.application_card import ApplicationCard

Builder.load_string(
    """
<ApplicationsScreen>:
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
                on_release: root.go_home()
            Label:
                text: "MES APPLICATIONS"
                bold: True
                font_size: "18sp"
                color: 1, 1, 1, 1

        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: card_list
                orientation: "vertical"
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: "+  Créer"
            size_hint_y: None
            height: dp(52)
            background_normal: ""
            background_color: 0.30, 0.45, 0.95, 1
            color: 1, 1, 1, 1
            font_size: "15sp"
            on_release: root.go_to_builder()
    """
)


class ApplicationsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = ApplicationService()

    def on_pre_enter(self, *args):
        self.refresh_list()

    def go_home(self):
        self.manager.current = ScreenNames.HOME

    def go_to_builder(self):
        self.manager.current = ScreenNames.APPLICATION_BUILDER

    def refresh_list(self):
        container = self.ids.card_list
        container.clear_widgets()
        applications = self._service.list_applications()

        if not applications:
            container.add_widget(
                Label(
                    text="Aucune application pour le moment.",
                    color=(0.6, 0.62, 0.68, 1),
                    size_hint_y=None,
                    height=dp(40),
                )
            )
            return

        for application in applications:
            stats = self._service.get_stats(application.id)
            card = ApplicationCard(
                app_id=application.id,
                app_name=application.name,
                icon=application.icon,
                entity_count=stats["entities"],
                record_count=stats["records"],
            )
            card.bind(on_release=lambda _inst, app=application: self.open_application(app))
            container.add_widget(card)

    def open_application(self, application):
        entity_builder = self.manager.get_screen(ScreenNames.ENTITY_BUILDER)
        entity_builder.set_application(application)
        self.manager.current = ScreenNames.ENTITY_BUILDER
