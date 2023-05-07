from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import random



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
        generate_button = Button(text='Generate')
        generate_button.bind(on_press=self.generate_private_key)
        self.add_widget(generate_button)

        # Generate an initial private key
        self.generate_private_key()

    def generate_private_key(self, *args):
        # Generate a private key based on the selected number of words
        word_list = [
            'apple', 'banana', 'cherry', 'date', 'eggplant', 'fig', 'grape',
            'honey', 'ice cream', 'juice', 'kiwi', 'lemon', 'mango',
            'nectarine', 'orange', 'peach', 'quince', 'raspberry',
            'strawberry', 'tangerine', 'umbrella', 'violet', 'watermelon',
            'xylophone', 'yellow', 'zebra'
        ]
        words = random.sample(word_list, self.num_words)
        private_key = ' '.join(words)

        # Display the private key
        self.private_key_label.text = 'Private Key:'
        words_box = self.children[1].children[0]
        words_box.clear_widgets()
        for index, word in enumerate(words):
            word_layout = BoxLayout(orientation='vertical',
                                    spacing=2,
                                    size_hint_y=None)
            word_layout.add_widget(
                Label(text=f'{index+1}. {word}', font_size='20sp'))
            words_box.add_widget(word_layout)
