"""Instructions screen showing spectrogram explanation"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main = FloatLayout()
        with main.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=main.size, pos=main.pos)
        main.bind(size=self._update_rect, pos=self._update_rect)
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text='Spectrograms display the frequency and amplitude of sound',
            size_hint=(1, 0.1),
            font_size='28sp',
            color=(0, 0.5, 0, 1),
            bold=True,
            halign='center'
        )
        title.bind(size=title.setter('text_size'))
        content.add_widget(title)
        
        # Main image
        img = Image(source='assets/example.png', size_hint=(1, 0.7))
        content.add_widget(img)
        
        # Back button
        back_box = BoxLayout(size_hint=(1, 0.2))
        back_btn = Button(
            background_normal='assets/Arrow.png',
            background_down='assets/Arrow.png',
            size_hint=(0.15, 1),
            pos_hint={'center_x': 0.5}
        )
        back_btn.bind(on_press=lambda x: self.manager.go_to('home'))
        back_box.add_widget(Widget())
        back_box.add_widget(back_btn)
        back_box.add_widget(Widget())
        content.add_widget(back_box)
        
        main.add_widget(content)
        self.add_widget(main)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
