"""Écran Field Builder : liste et création des champs (Field) d'une
entité. Complète la chaîne Application → Entity → Field."""

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from core.constants import FieldType, ScreenNames
from core.exceptions import ValidationError
from services.field_service import FieldService
from widgets.field_row import FieldRow

Builder.load_string(
    """
<FieldBuilderScreen>:
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
                font_size: "16sp"
                halign: "left"
                valign: "middle"
                text_size: self.size
                color: 1, 1, 1, 1
                shorten: True

        Label:
            text: "CHAMPS"
            font_size: "13sp"
            color: 0.6, 0.62, 0.68, 1
            size_hint_y: None
            height: dp(20)
            halign: "left"
            text_size: self.size

        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: field_list
                orientation: "vertical"
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: "+  Ajouter un champ"
            size_hint_y: None
            height: dp(52)
            background_normal: ""
            background_color: 0.30, 0.45, 0.95, 1
            color: 1, 1, 1, 1
            font_size: "15sp"
            on_release: root.open_create_popup()
    """
)


class FieldBuilderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = FieldService()
        self._entity = None

    def set_entity(self, entity):
        """Doit être appelée avant chaque navigation vers cet écran."""
        self._entity = entity
        self.ids.title_label.text = f"🧩  {entity.name.upper()}"

    def on_pre_enter(self, *args):
        if self._entity is not None:
            self.refresh_list()

    def go_back(self):
        self.manager.current = ScreenNames.ENTITY_BUILDER

    def refresh_list(self):
        container = self.ids.field_list
        container.clear_widgets()
        fields = self._service.list_fields(self._entity.id)

        if not fields:
            container.add_widget(
                Label(
                    text="Aucun champ pour le moment.",
                    color=(0.6, 0.62, 0.68, 1),
                    size_hint_y=None,
                    height=dp(40),
                )
            )
            return

        for f in fields:
            row = FieldRow(
                field_id=f.id,
                field_name=f.name,
                field_label=f.label,
                field_type=f.type,
                required=f.required,
            )
            row.bind(on_move_up=lambda _i, fid=f.id: self._move(fid, -1))
            row.bind(on_move_down=lambda _i, fid=f.id: self._move(fid, 1))
            row.bind(on_delete=lambda _i, fid=f.id: self._delete(fid))
            container.add_widget(row)

    def _move(self, field_id, direction):
        if direction < 0:
            self._service.move_up(self._entity.id, field_id)
        else:
            self._service.move_down(self._entity.id, field_id)
        self.refresh_list()

    def _delete(self, field_id):
        self._service.delete_field(field_id)
        self.refresh_list()

    def open_create_popup(self):
        layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(16))

        label_input = TextInput(
            hint_text="Ex : Adresse email", multiline=False,
            size_hint_y=None, height=dp(44),
        )
        type_spinner = Spinner(
            text=FieldType.TEXT, values=FieldType.ALL,
            size_hint_y=None, height=dp(44),
        )
        required_row = BoxLayout(size_hint_y=None, height=dp(32), spacing=dp(8))
        required_checkbox = CheckBox(size_hint_x=None, width=dp(32))
        required_row.add_widget(required_checkbox)
        required_row.add_widget(Label(text="Champ obligatoire", color=(1, 1, 1, 1)))

        error_label = Label(text="", color=(1, 0.4, 0.4, 1), size_hint_y=None, height=dp(24))

        layout.add_widget(Label(text="Libellé", size_hint_y=None, height=dp(20), color=(1, 1, 1, 1)))
        layout.add_widget(label_input)
        layout.add_widget(Label(text="Type", size_hint_y=None, height=dp(20), color=(1, 1, 1, 1)))
        layout.add_widget(type_spinner)
        layout.add_widget(required_row)
        layout.add_widget(error_label)

        buttons = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(10))
        cancel_button = Button(text="Annuler")
        create_button = Button(text="Créer")
        buttons.add_widget(cancel_button)
        buttons.add_widget(create_button)
        layout.add_widget(buttons)

        popup = Popup(title="Ajouter un champ", content=layout, size_hint=(0.9, 0.6))

        def do_create(*_):
            try:
                self._service.create_field(
                    entity_id=self._entity.id,
                    label=label_input.text,
                    field_type=type_spinner.text,
                    required=required_checkbox.active,
                )
                popup.dismiss()
                self.refresh_list()
            except ValidationError as exc:
                error_label.text = str(exc)

        create_button.bind(on_release=do_create)
        cancel_button.bind(on_release=popup.dismiss)
        popup.open()