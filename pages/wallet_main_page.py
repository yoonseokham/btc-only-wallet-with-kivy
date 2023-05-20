from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy_garden.qrcode import QRCodeWidget


class WalletMainPage(BoxLayout):
    def __init__(self, wallet, **kwargs):
        self.wallet = wallet
        super().__init__(orientation='vertical', **kwargs)

        # Create a label for the page title
        title_label = Label(text='Wallet Main Page')
        self.add_widget(title_label)

        # Create a button for receiving BTC
        receive_button = Button(text='Receive BTC')
        receive_button.bind(on_press=self.show_address_popup)
        self.add_widget(receive_button)

        # Create a button for sending BTC
        send_button = Button(text='Send BTC')
        send_button.bind(on_press=self.send_btc)
        self.add_widget(send_button)

        # Create a button for showing XPub
        xpub_button = Button(text='XPub')
        xpub_button.bind(on_press=self.show_xpub_popup)
        self.add_widget(xpub_button)

    def show_address_popup(self, *args):
        # Create a pop-up with the address and QR code
        address = self.wallet.get_address()

        # Create the content layout
        content_layout = BoxLayout(
            orientation='vertical',
            spacing='10dp',
            padding='10dp',
        )

        # Add the address label
        address_label = Label(
            text=f"Receive BTC to:\n{address}",
            size_hint_y=None,
            valign='middle',
            text_size=(400, None),
        )
        address_label.bind(texture_size=address_label.setter('size'))
        content_layout.add_widget(address_label)

        # Create the QR code for the address
        qr_code_widget = self.generate_qrcode_with_string(address)
        content_layout.add_widget(qr_code_widget)

        # Create the scrollable view
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(content_layout)

        # Create the popup
        popup = Popup(title='Receive BTC',
                      content=scroll_view,
                      size_hint=(None, None),
                      size=(500, 500))
        popup.open()

    def send_btc(self, *args):
        # Handle the logic for sending BTC
        print("Send BTC button pressed!")

    def show_xpub_popup(self, *args):
        # Create a pop-up with the xpub
        content_layout = BoxLayout(
            orientation='vertical',
            spacing='10dp',
            padding='10dp',
        )
        xpub = self.wallet.get_xpub()
        content_label = Label(
            text=f"Extended Public Key (xpub):\n{xpub}",
            size_hint_y=None,
            valign='middle',
            text_size=(400, None),
        )
        content_label.bind(texture_size=content_label.setter('size'))
        content_layout.add_widget(content_label)
        # Create the QR code for the address
        qr_code_widget = self.generate_qrcode_with_string(xpub)
        content_layout.add_widget(qr_code_widget)
        scroll_view = ScrollView(size_hint=(None, None), size=(500, 400))
        scroll_view.add_widget(content_layout)
        popup = Popup(
            title='XPub',
            content=scroll_view,
            size_hint=(None, None),
            size=(600, 500),
        )
        popup.open()

    @staticmethod
    def generate_qrcode_with_string(data):
        return QRCodeWidget(data=data)
