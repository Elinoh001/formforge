"""Ligne réutilisable affichant un champ (Field) avec ses actions
(monter, descendre, supprimer) dans le Field Builder."""

from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_string(
    """
<FieldRow>:
    size_hint_y: None
    height: dp(56)
    padding: dp(12), dp(8)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: 0.13, 0.14, 0.18, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]

    BoxLayout:
        orientation: "vertical"
        Label:
            text: root.field_label + ("  *" if root.required else "")
            font_size: "15sp"
            bold: True
            halign: "left"
            valign: "middle"
            text_size: self.size
            color: 1, 1, 1, 1
        Label:
            text: root.field_name + "  ·  " + root.field_type
            font_size: "11sp"
            halign: "left"
            valign: "middle"
            text_size: self.size
            color: 0.6, 0.62, 0.68, 1

    Button:
        text: "↑"
        size_hint_x: None
        width: dp(36)
        background_normal: ""
        background_color: 0.2, 0.21, 0.26, 1
        color: 1, 1, 1, 1
        on_release: root.dispatch("on_move_up")

    Button:
        text: "↓"
        size_hint_x: None
        width: dp(36)
        background_normal: ""
        background_color: 0.2, 0.21, 0.26, 1
        color: 1, 1, 1, 1
        on_release: root.dispatch("on_move_down")

    Button:
        text: "✕"
        size_hint_x: None
        width: dp(36)
        background_normal: ""
        background_color: 0.45, 0.18, 0.2, 1
        color: 1, 1, 1, 1
        on_release: root.dispatch("on_delete")
    """
)


class FieldRow(BoxLayout):
    field_id = StringProperty("")
    field_name = StringProperty("")
    field_label = StringProperty("")
    field_type = StringProperty("text")
    required = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type("on_move_up")
        self.register_event_type("on_move_down")
        self.register_event_type("on_delete")
        super().__init__(**kwargs)

    def on_move_up(self):
        pass

    def on_move_down(self):
        pass

    def on_delete(self):
        pass