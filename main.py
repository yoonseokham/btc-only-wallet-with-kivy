import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy import logger

from pages import create_wallet_page
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')


class BTCWalletApp(App):
    def build(self):
        # Create a BoxLayout for the main interface
        layout = BoxLayout(orientation='vertical')

        # Check if the private key file exists
        if os.path.isfile('private_key.txt'):
            # Read the private key from the file
            with open('private_key.txt', 'r') as f:
                private_key = f.read()

            # Display the private key
            label = Label(text='Private Key: ' + private_key)
            layout.add_widget(label)
        else:
            logger.Logger.info('there is no private key')
            # Add a label to the layout
            label = Label(text='BTC Wallet App')
            layout.add_widget(label)

            # Add an 'Import Wallet' button
            import_button = Button(text='Import Wallet')
            layout.add_widget(import_button)

            # Add a 'Create Wallet' button
            create_button = Button(text='Create Wallet')
            create_button.bind(on_press=self.go_to_create_wallet_page)
            layout.add_widget(create_button)

        return layout

    def go_to_create_wallet_page(self, *args):
        # Switch to the create wallet page
        self.root.clear_widgets()
        self.root.add_widget(create_wallet_page.CreateWalletPage())


if __name__ == '__main__':
    BTCWalletApp().run()
