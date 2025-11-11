"""Home screen with frog selection grid"""
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.app import App
from screens.frog_data import FROGS


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Triple-tap exit functionality
        self.tap_count = 0
        self.tap_timer = None
        
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
        grid.bind(size=self._update_grid_children)
        
        # Instructions button
        inst_box = BoxLayout(orientation='vertical', spacing=5)
        
        # Button container to maintain alignment
        inst_btn_container = BoxLayout(size_hint=(1, 0.85))
        inst_btn = Button(background_normal='assets/App_overview.png', 
                         background_down='assets/App_overview.png',
                         size_hint=(None, None))
        inst_btn.bind(on_press=lambda x: self.manager.go_to('instructions'))
        inst_btn_container.bind(size=lambda i, v: self._update_frog_button_size(inst_btn, i))
        inst_btn_container.add_widget(inst_btn)
        inst_box.add_widget(inst_btn_container)
        
        inst_label = Label(text="How spectrograms\nshow sound", font_size='22sp', 
                          color=(1, 1, 1, 1), size_hint=(1, 0.15), halign='center', valign='top',
                          text_size=(None, None), max_lines=2)
        inst_label.bind(width=lambda l, w: setattr(l, 'text_size', (w, None)))
        inst_box.add_widget(inst_label)
        grid.add_widget(inst_box)
        
        # Frog buttons
        for frog in FROGS:
            frog_box = BoxLayout(orientation='vertical', spacing=5)
            
            # Button container to maintain alignment
            btn_container = BoxLayout(size_hint=(1, 0.85))
            btn = Button(background_normal=frog['photo'], 
                        background_down=frog['photo'],
                        size_hint=(None, None))
            btn.bind(on_press=lambda x, f=frog: self.manager.show_frog(f))
            btn_container.bind(size=lambda i, v, b=btn: self._update_frog_button_size(b, i))
            btn_container.add_widget(btn)
            frog_box.add_widget(btn_container)
            
            lbl = Label(text=frog['name'], font_size='22sp', 
                       color=(1, 1, 1, 1), size_hint=(1, 0.15), halign='center', valign='top',
                       text_size=(None, None), max_lines=2)
            lbl.bind(width=lambda l, w: setattr(l, 'text_size', (w, None)))
            frog_box.add_widget(lbl)
            grid.add_widget(frog_box)
        
        # Mystery frog button
        mystery_box = BoxLayout(orientation='vertical', spacing=5)
        
        # Button container to maintain alignment
        mystery_btn_container = BoxLayout(size_hint=(1, 0.85))
        mystery_btn = Button(background_normal='assets/UnknownFrog.png',
                            background_down='assets/UnknownFrog.png',
                            size_hint=(None, None))
        mystery_btn.bind(on_press=lambda x: self.manager.go_to('mystery'))
        mystery_btn_container.bind(size=lambda i, v: self._update_frog_button_size(mystery_btn, i))
        mystery_btn_container.add_widget(mystery_btn)
        mystery_box.add_widget(mystery_btn_container)
        
        mystery_label = Label(text="Mystery Frog", font_size='22sp', 
                             color=(1, 1, 1, 1), size_hint=(1, 0.15), halign='center', valign='top',
                             text_size=(None, None), max_lines=2)
        mystery_label.bind(width=lambda l, w: setattr(l, 'text_size', (w, None)))
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
        self.grid = grid
    
    def _update_frog_button_size(self, button, container):
        """Maintain square aspect ratio and center buttons"""
        if container.width > 0 and container.height > 0:
            size = min(container.width, container.height)
            button.size = (size, size)
            # Center the button
            button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    
    def _update_grid_children(self, instance, value):
        """Ensure buttons maintain square aspect ratio"""
        # This method is kept for compatibility but button sizing is now handled by _update_frog_button_size
        pass
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_touch_down(self, touch):
        """Handle triple-tap exit in top-left corner (100x100 hot zone)"""
        # Check if touch is in the hot zone (top-left 100x100 pixels)
        if touch.x < 100 and (self.height - touch.y) < 100:
            self.tap_count += 1
            
            # Start or restart the timer
            if self.tap_timer:
                self.tap_timer.cancel()
            self.tap_timer = Clock.schedule_once(self._reset_tap_count, 5)
            
            # Check if we've reached 3 taps
            if self.tap_count >= 3:
                self._show_exit_confirmation()
                return True  # Consume the touch event
        
        # Pass touch to children widgets
        return super().on_touch_down(touch)
    
    def _reset_tap_count(self, dt):
        """Reset tap counter after timeout"""
        self.tap_count = 0
        self.tap_timer = None
    
    def _show_exit_confirmation(self):
        """Show confirmation dialog before exiting"""
        # Reset tap count
        self.tap_count = 0
        if self.tap_timer:
            self.tap_timer.cancel()
            self.tap_timer = None
        
        # Create confirmation popup
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        content.add_widget(Label(text='Do you want to exit the application?', 
                                font_size='20sp', halign='center'))
        
        buttons = BoxLayout(spacing=10, size_hint=(1, 0.3))
        
        # Create popup first so we can reference it in button callbacks
        popup = Popup(title='Exit Application',
                     content=content,
                     size_hint=(0.6, 0.4),
                     auto_dismiss=False)
        
        yes_btn = Button(text='Yes', background_color=(0.8, 0.2, 0.2, 1))
        yes_btn.bind(on_press=lambda x: self._exit_app(popup))
        
        no_btn = Button(text='No', background_color=(0.2, 0.8, 0.2, 1))
        no_btn.bind(on_press=popup.dismiss)
        
        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        content.add_widget(buttons)
        
        popup.open()
    
    def _exit_app(self, popup):
        """Exit the application"""
        popup.dismiss()
        App.get_running_app().stop()
