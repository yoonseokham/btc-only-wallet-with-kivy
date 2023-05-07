from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from pages import generate_private_key_page


class CreateWalletPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Create a label for the page title
        title_label = Label(text='Create Wallet')
        self.add_widget(title_label)

        # Create two buttons to select the number of words
        self.num_words = 12
        self.twelve_button = Button(text='12 Words',
                                    background_color=(0, 1, 0, 1))
        self.twelve_button.bind(on_press=lambda x: self.set_num_words(12))
        self.add_widget(self.twelve_button)

        self.twentyfour_button = Button(text='24 Words',
                                        background_color=(1, 0, 0, 1))
        self.twentyfour_button.bind(on_press=lambda x: self.set_num_words(24))
        self.add_widget(self.twentyfour_button)

        # Create a button to generate the private key
        generate_button = Button(text='Generate Private Key')
        generate_button.bind(on_press=self.go_to_generate_private_key_page)
        self.add_widget(generate_button)

    def set_num_words(self, num_words):
        self.num_words = num_words

        # Update button state
        if num_words == 12:
            self.twelve_button.background_color = (0, 1, 0, 1)
            self.twentyfour_button.background_color = (1, 0, 0, 1)
        else:
            self.twelve_button.background_color = (1, 0, 0, 1)
            self.twentyfour_button.background_color = (0, 1, 0, 1)

    def go_to_generate_private_key_page(self, *args):
        # Switch to the generate and show private key page
        self.parent.add_widget(
            generate_private_key_page.GeneratePrivateKeyPage(
                num_words=self.num_words))
        self.parent.remove_widget(self)
