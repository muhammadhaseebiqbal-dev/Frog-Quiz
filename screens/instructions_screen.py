"""Instructions screen showing spectrogram explanation"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line


class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main = FloatLayout()
        with main.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=main.size, pos=main.pos)
        main.bind(size=self._update_rect, pos=self._update_rect)
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='Spectrograms display the frequency and amplitude of sound',
            size_hint=(1, 0.08),
            font_size='28sp',
            color=(0, 0.5, 0, 1),
            bold=True,
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        content.add_widget(title)
        
        # Top info boxes (frequency and amplitude explanations)
        top_boxes = BoxLayout(size_hint=(1, 0.18), spacing=20)
        
        # Frequency box with background
        freq_box = FloatLayout(size_hint=(0.5, 1))
        with freq_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.freq_rect = Rectangle()
        freq_box.bind(pos=lambda i, v: setattr(self.freq_rect, 'pos', i.pos),
                     size=lambda i, v: setattr(self.freq_rect, 'size', i.size))
        
        # Frequency label with simpler text
        freq_label = Label(
            text='Sounds are vibrations and the number of vibrations per second determines the [b]frequency[/b] or pitch of a sound.\n\n[b]Low pitch:[/b] drum roll, growl\n[b]High pitch:[/b] whistle, jingling keys',
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='16sp',
            color=(0, 0, 0, 1),
            halign='left',
            valign='middle',
            markup=True
        )
        freq_label.bind(width=lambda l, w: setattr(l, 'text_size', (w, None)))
        freq_box.add_widget(freq_label)
        top_boxes.add_widget(freq_box)
        
        # Amplitude box with background
        amp_box = FloatLayout(size_hint=(0.5, 1))
        with amp_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.amp_rect = Rectangle()
        amp_box.bind(pos=lambda i, v: setattr(self.amp_rect, 'pos', i.pos),
                    size=lambda i, v: setattr(self.amp_rect, 'size', i.size))
        
        # Amplitude label with simpler text
        amp_label = Label(
            text='The size of sound waves determines [b]amplitude[/b] — the larger the wave, the louder the sound.\n\n[b]Low amplitude:[/b] whispering\n[b]High amplitude:[/b] yelling',
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='16sp',
            color=(0, 0, 0, 1),
            halign='left',
            valign='middle',
            markup=True
        )
        amp_label.bind(width=lambda l, w: setattr(l, 'text_size', (w, None)))
        amp_box.add_widget(amp_label)
        top_boxes.add_widget(amp_box)
        
        content.add_widget(top_boxes)
        
        # Main spectrogram image (larger)
        img = Image(source='assets/example.png', size_hint=(1, 0.5), allow_stretch=True, keep_ratio=True)
        content.add_widget(img)
        
        # Bottom section: Back button and explanation boxes
        bottom_section = BoxLayout(size_hint=(1, 0.24), spacing=20)
        
        # Back button - maintain square aspect
        back_container = BoxLayout(size_hint=(0.2, 1))
        back_btn = Button(
            background_normal='assets/Arrow.png',
            background_down='assets/Arrow.png',
            size_hint=(None, None)
        )
        back_btn.bind(on_press=lambda x: self.manager.go_to('home'))
        back_container.bind(size=lambda i, v: self._update_button_size(back_btn, i))
        back_container.add_widget(back_btn)
        bottom_section.add_widget(back_container)
        
        # Green box explanation
        green_box = FloatLayout(size_hint=(0.4, 1))
        
        # Add background
        with green_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.green_bg = Rectangle()
        green_box.bind(pos=lambda i, v: setattr(self.green_bg, 'pos', i.pos),
                      size=lambda i, v: setattr(self.green_bg, 'size', i.size))
        
        green_label = Label(
            text='The call in the [b]green box[/b] has a higher [b]frequency[/b].',
            size_hint=(0.85, 0.85),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='18sp',
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle',
            markup=True
        )
        green_label.bind(width=lambda l, w: setattr(l, 'text_size', (w, None)))
        
        # Draw green border
        with green_box.canvas.after:
            Color(0.3, 0.69, 0.31, 1)  # Green color
            self.green_line = Line(width=4)
        green_box.bind(pos=self._update_green_border, size=self._update_green_border)
        
        green_box.add_widget(green_label)
        bottom_section.add_widget(green_box)
        
        # Yellow box explanation
        yellow_box = FloatLayout(size_hint=(0.4, 1))
        
        # Add background
        with yellow_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.yellow_bg = Rectangle()
        yellow_box.bind(pos=lambda i, v: setattr(self.yellow_bg, 'pos', i.pos),
                       size=lambda i, v: setattr(self.yellow_bg, 'size', i.size))
        
        yellow_label = Label(
            text='The call in the [b]yellow box[/b] is higher in [b]amplitude[/b].',
            size_hint=(0.85, 0.85),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='18sp',
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle',
            markup=True
        )
        yellow_label.bind(width=lambda l, w: setattr(l, 'text_size', (w, None)))
        
        # Draw yellow border
        with yellow_box.canvas.after:
            Color(1, 0.84, 0, 1)  # Yellow color
            self.yellow_line = Line(width=4)
        yellow_box.bind(pos=self._update_yellow_border, size=self._update_yellow_border)
        
        yellow_box.add_widget(yellow_label)
        bottom_section.add_widget(yellow_box)
        
        content.add_widget(bottom_section)
        
        main.add_widget(content)
        self.add_widget(main)
    
    def _update_button_size(self, button, container):
        """Maintain square aspect ratio for buttons"""
        if container.width > 0 and container.height > 0:
            size = min(container.width, container.height)
            button.size = (size, size)
            button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    
    def _update_green_border(self, instance, value):
        """Update green border rectangle"""
        self.green_line.rectangle = (instance.x, instance.y, instance.width, instance.height)
    
    def _update_yellow_border(self, instance, value):
        """Update yellow border rectangle"""
        self.yellow_line.rectangle = (instance.x, instance.y, instance.width, instance.height)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
