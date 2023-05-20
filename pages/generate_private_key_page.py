from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from pages import wallet_interface
from pages import wallet_main_page


class GeneratePrivateKeyPage(BoxLayout):
    def __init__(self, num_words=12, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.num_words = num_words

        # Create a label for the page title
        title_label = Label(text='Generate Private Key')
        self.add_widget(title_label)

        # Create a box layout to contain the generated words
        words_box = BoxLayout(orientation='vertical',
                              spacing=10,
                              size_hint_y=None)
        words_box.bind(minimum_height=words_box.setter('height'))

        # Create a scroll view to contain the words box
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(words_box)
        self.add_widget(scroll_view)

        # Create a label to display the generated private key
        self.private_key_label = Label(text='Private Key:')
        words_box.add_widget(self.private_key_label)

        # Create a button to generate a new private key
        generate_button = Button(text='Regenerate')
        generate_button.bind(on_press=self.generate_private_key)
        self.add_widget(generate_button)

        # Generate an initial private key
        self.start_wallet_button = Button(text='Start Wallet', disabled=True)
        self.start_wallet_button.bind(on_press=self.go_to_wallet_main_page)
        self.add_widget(self.start_wallet_button)

    def generate_private_key(self, *args):
        self.new_wallet = wallet_interface.WalletInterface(
            length=self.num_words)
        private_key_list = list(self.new_wallet.mnemonic.split())
        self.start_wallet_button.disabled = False
        # Display the private key
        self.private_key_label.text = 'press button to generate private key:'
        words_box = None
        for i in self.children:
            if type(i) == ScrollView:
                words_box = i.children[0]
        words_box.clear_widgets()
        for index, word in enumerate(private_key_list):
            word_layout = BoxLayout(orientation='vertical',
                                    spacing=2,
                                    size_hint_y=None)
            word_layout.add_widget(
                Label(text=f'{index+1}. {word}', font_size='20sp'))
            words_box.add_widget(word_layout)

    def go_to_wallet_main_page(self, *args):
        # Switch to the wallet main page
        self.parent.add_widget(wallet_main_page.WalletMainPage(
            self.new_wallet))
        self.parent.remove_widget(self)
