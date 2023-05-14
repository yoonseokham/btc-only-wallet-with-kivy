from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class WalletMainPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Create a label for the page title
        title_label = Label(text='Wallet Main Page')
        self.add_widget(title_label)

        # Create a button for receiving BTC
        receive_button = Button(text='Receive BTC')
        receive_button.bind(on_press=self.receive_btc)
        self.add_widget(receive_button)

        # Create a button for sending BTC
        send_button = Button(text='Send BTC')
        send_button.bind(on_press=self.send_btc)
        self.add_widget(send_button)

    def receive_btc(self, *args):
        # Handle the logic for receiving BTC
        print("Receive BTC button pressed!")

    def send_btc(self, *args):
        # Handle the logic for sending BTC
        print("Send BTC button pressed!")
