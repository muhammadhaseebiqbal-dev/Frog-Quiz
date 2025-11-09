"""Home screen with frog selection grid"""
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from screens.frog_data import FROGS


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        main = FloatLayout()
        
        # Background color
        with main.canvas.before:
            Color(0.18, 0.54, 0.34, 1)
            self.rect = Rectangle(size=main.size, pos=main.pos)
        main.bind(size=self._update_rect, pos=self._update_rect)
        
        # Content container
        content = BoxLayout(orientation='vertical', padding=[20, 20], spacing=20,
                           size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Title
        title = Label(
            text='Select a frog to see and hear its call',
            size_hint=(1, 0.1),
            font_size='36sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        content.add_widget(title)
        
        # Grid of buttons (5 columns: instructions + 8 frogs + mystery)
        grid = GridLayout(cols=5, spacing=25, size_hint=(1, 0.8), padding=[50, 0])
        
        # Instructions button
        inst_box = BoxLayout(orientation='vertical', spacing=5)
        inst_btn = Button(background_normal='assets/App_overview.png', 
                         background_down='assets/App_overview.png',
                         size_hint=(1, 1))
        inst_btn.bind(on_press=lambda x: self.manager.go_to('instructions'))
        inst_box.add_widget(inst_btn)
        inst_label = Label(text="How spectrograms\nshow sound", font_size='20sp', 
                          color=(1, 1, 1, 1), size_hint=(1, 0.15), halign='center')
        inst_label.bind(size=inst_label.setter('text_size'))
        inst_box.add_widget(inst_label)
        grid.add_widget(inst_box)
        
        # Frog buttons
        for frog in FROGS:
            frog_box = BoxLayout(orientation='vertical', spacing=5)
            btn = Button(background_normal=frog['photo'], 
                        background_down=frog['photo'],
                        size_hint=(1, 1))
            btn.bind(on_press=lambda x, f=frog: self.manager.show_frog(f))
            frog_box.add_widget(btn)
            
            lbl = Label(text=frog['name'], font_size='20sp', 
                       color=(1, 1, 1, 1), size_hint=(1, 0.15), halign='center')
            lbl.bind(size=lbl.setter('text_size'))
            frog_box.add_widget(lbl)
            grid.add_widget(frog_box)
        
        # Mystery frog button
        mystery_box = BoxLayout(orientation='vertical', spacing=5)
        mystery_btn = Button(background_normal='assets/UnknownFrog.png',
                            background_down='assets/UnknownFrog.png',
                            size_hint=(1, 1))
        mystery_btn.bind(on_press=lambda x: self.manager.go_to('mystery'))
        mystery_box.add_widget(mystery_btn)
        mystery_label = Label(text="Mystery Frog", font_size='20sp', 
                             color=(1, 1, 1, 1), size_hint=(1, 0.15), halign='center')
        mystery_label.bind(size=mystery_label.setter('text_size'))
        mystery_box.add_widget(mystery_label)
        grid.add_widget(mystery_box)
        
        content.add_widget(grid)
        
        # App Info button
        info_btn = Button(
            text='App Info',
            size_hint=(0.2, 0.08),
            pos_hint={'center_x': 0.5},
            background_color=(0.3, 0.69, 0.31, 1),
            font_size='20sp'
        )
        info_btn.bind(on_press=lambda x: self.manager.go_to('app_info'))
        content.add_widget(info_btn)
        
        main.add_widget(content)
        self.add_widget(main)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
