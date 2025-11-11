"""App info screen"""
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class AppInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main = FloatLayout()
        with main.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=main.size, pos=main.pos)
        main.bind(size=self._update_rect, pos=self._update_rect)
        
        # Main container
        container = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Title (fixed at top)
        title = Label(text='App Info', size_hint=(1, 0.1), font_size='36sp', color=(0, 0, 0, 1), bold=True)
        container.add_widget(title)
        
        # Scrollable content area
        scroll = ScrollView(size_hint=(1, 0.75), do_scroll_x=False, do_scroll_y=True)
        
        # Content inside scroll view
        scroll_content = BoxLayout(orientation='vertical', size_hint_y=None, padding=(10, 10), spacing=10)
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        info = Label(
            text='This app was created and designed by Katie Howard\n'
                 'for the exhibition "Litoria\'s Wetland World".\n\n'
                 'Sound files were provided by the Arthur Rylah Institute\n'
                 'for Environmental Research (DEECA) and compiled with\n'
                 'help from Louise Durkin.\n\n'
                 'Spectrograms were created using PASE\n'
                 '(Python-Audio-Spectrogram-Explorer).\n\n'
                 'All photos provided by Katie Howard except for those\n'
                 'listed below, which are used with permission from:\n'
                 '- Zak Atkins: Peron\'s Tree Frog\n'
                 '- Geoff Heard: Pobblebonk Frog and Spotted Marsh Frog',
            size_hint_y=None,
            font_size='18sp',
            color=(0, 0, 0, 1),
            halign='center',
            valign='top',
            padding=(20, 20)
        )
        info.bind(width=lambda l, w: setattr(l, 'text_size', (w - 40, None)))
        info.bind(texture_size=lambda l, s: setattr(l, 'height', s[1]))
        
        scroll_content.add_widget(info)
        scroll.add_widget(scroll_content)
        container.add_widget(scroll)
        
        # Back button at bottom (fixed) - maintain square aspect
        back_box = BoxLayout(size_hint=(1, 0.15))
        back_btn_container = BoxLayout(size_hint=(0.15, 1))
        back_btn = Button(
            background_normal='assets/Arrow.png',
            background_down='assets/Arrow.png',
            size_hint=(None, None)
        )
        back_btn.bind(on_press=lambda x: self.manager.go_to('home'))
        back_btn_container.bind(size=lambda i, v: self._update_button_size(back_btn, i))
        back_btn_container.add_widget(back_btn)
        back_box.add_widget(Widget())
        back_box.add_widget(back_btn_container)
        back_box.add_widget(Widget())
        container.add_widget(back_box)
        
        main.add_widget(container)
        self.add_widget(main)
    
    def _update_button_size(self, button, container):
        """Maintain square aspect ratio for buttons"""
        if container.width > 0 and container.height > 0:
            size = min(container.width, container.height)
            button.size = (size, size)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
