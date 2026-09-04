"""Carte réutilisable affichant le résumé d'une application dans une liste."""

from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

Builder.load_string(
    """
<ApplicationCard>:
    orientation: "vertical"
    size_hint_y: None
    height: dp(88)
    padding: dp(16), dp(12)
    spacing: dp(4)
    canvas.before:
        Color:
            rgba: 0.13, 0.14, 0.18, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]

    Label:
        text: root.icon + "  " + root.app_name
        font_size: "17sp"
        bold: True
        halign: "left"
        valign: "middle"
        text_size: self.size
        color: 1, 1, 1, 1
        size_hint_y: None
        height: dp(28)

    Label:
        text: f"{root.entity_count} entité(s)  ·  {root.record_count} enregistrement(s)"
        font_size: "13sp"
        halign: "left"
        valign: "middle"
        text_size: self.size
        color: 0.7, 0.72, 0.78, 1
    """
)


class ApplicationCard(ButtonBehavior, BoxLayout):
    """Carte cliquable. Le parent se connecte via bind(on_release=...)."""

    app_id = StringProperty("")
    app_name = StringProperty("")
    icon = StringProperty("📁")
    entity_count = NumericProperty(0)
    record_count = NumericProperty(0)
