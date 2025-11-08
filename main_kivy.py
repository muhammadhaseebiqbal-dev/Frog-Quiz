# Kivy-based Android APK Entry Point
# This is a simplified version that can be built with Buildozer

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import platform

class FrogQuizApp(App):
    def build(self):
        Window.clearcolor = (0.18, 0.54, 0.34, 1)  # Green background
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text='Frog Quiz Educational App',
            size_hint=(1, 0.2),
            font_size='32sp',
            bold=True
        )
        layout.add_widget(title)
        
        # Info message
        info = Label(
            text='This is a simplified Kivy version for Android.\n\n'
                 'The full NiceGUI web version with videos and interactive content\n'
                 'is available at the hosted web address.\n\n'
                 'NiceGUI cannot be compiled to APK due to complex dependencies.\n'
                 'Use the Progressive Web App (PWA) for full functionality.',
            size_hint=(1, 0.6),
            font_size='18sp',
            halign='center',
            valign='middle'
        )
        info.bind(size=info.setter('text_size'))
        layout.add_widget(info)
        
        # Exit button
        exit_btn = Button(
            text='Exit',
            size_hint=(1, 0.2),
            font_size='24sp',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        exit_btn.bind(on_press=self.stop_app)
        layout.add_widget(exit_btn)
        
        return layout
    
    def stop_app(self, *args):
        App.get_running_app().stop()

if __name__ == '__main__':
    FrogQuizApp().run()
