from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy_garden.qrcode import QRCodeWidget

from kivy.core.window import Window


class SendBtcPopup(Popup):
    def __init__(self, wallet, **kwargs):
        super().__init__(**kwargs)
        self.title = "Send BTC"
        self.size_hint = (None, None)
        self.size = (500, 500)
        self.auto_dismiss = False
        self.wallet = wallet

        # Create a scroll view for the popup content
        scroll_view = ScrollView()

        # Create a grid layout for the scroll view content
        grid_layout = GridLayout(cols=1,
                                 spacing=10,
                                 size_hint_y=None,
                                 padding=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Create a text input for entering data
        self.text_input = TextInput(
            hint_text="Enter data",
            multiline=False,
            size_hint=(1, None),
            height=40,
            focus=False,
        )
        self.text_input.bind(focus=self.on_text_input_focus)
        grid_layout.add_widget(self.text_input)

        # Create a button to sign the data
        sign_button = Button(
            text="Sign",
            size_hint=(None, None),
            size=(100, 50),
        )
        sign_button.bind(on_press=self.sign_data)
        grid_layout.add_widget(sign_button)

        self.qr_code = QRCodeWidget(
            size_hint=(None, None),
            size=(350, 350),
        )
        grid_layout.add_widget(self.qr_code)

        # Create a button to close the popup
        close_button = Button(text="x", size_hint=(None, None), size=(50, 50))
        close_button.bind(on_press=self.dismiss)
        grid_layout.add_widget(close_button)
        scroll_view.add_widget(grid_layout)
        self.content = scroll_view

    def sign_data(self, *args):
        # Get the entered data
        data = self.text_input.text

        # Sign the data by adding 'hello' to it
        signed_data = self.wallet.sign_psbt(data)

        # Update the QR code with the signed data
        self.qr_code.data = signed_data

    def on_text_input_focus(self, instance, focused):
        if focused:
            Window.keyboard_mode = 'managed'
        else:
            Window.keyboard_mode = 'system'

    def on_keyboard_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':
            self.sign_data()
