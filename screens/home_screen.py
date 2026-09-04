"""Écran d'accueil de FormForge."""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from core.constants import ScreenNames

Builder.load_string(
    """
<HomeScreen>:
    canvas.before:
        Color:
            rgba: 0.07, 0.08, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(16)

        Widget:
            size_hint_y: None
            height: dp(30)

        Label:
            text: "FORMFORGE"
            font_size: "30sp"
            bold: True
            color: 1, 1, 1, 1
            size_hint_y: None
            height: dp(44)

        Label:
            text: "Construisez vos applications\\nsans écrire de code."
            font_size: "15sp"
            color: 0.75, 0.77, 0.82, 1
            size_hint_y: None
            height: dp(50)
            halign: "left"
            valign: "top"
            text_size: self.size

        Button:
            text: "+  Créer une application"
            size_hint_y: None
            height: dp(52)
            background_normal: ""
            background_color: 0.30, 0.45, 0.95, 1
            color: 1, 1, 1, 1
            font_size: "15sp"
            on_release: root.go_to_applications()

        Widget:
            size_hint_y: None
            height: dp(6)

        Button:
            text: "Mes applications  →"
            size_hint_y: None
            height: dp(48)
            background_normal: ""
            background_color: 0.15, 0.16, 0.20, 1
            color: 1, 1, 1, 1
            font_size: "14sp"
            on_release: root.go_to_applications()

        Widget:
    """
)


class HomeScreen(Screen):
    def go_to_applications(self):
        self.manager.current = ScreenNames.APPLICATIONS
