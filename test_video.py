"""
Quick test to verify video playback works
Run this to test if videos play without starting the full app
"""
import os
import platform

# Set audio driver BEFORE importing Kivy
if platform.system() == 'Windows':
    os.environ['SDL_AUDIODRIVER'] = 'directsound'
    os.environ['KIVY_AUDIO'] = 'sdl2'

from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class VideoTestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Video widget
        self.video = Video(source='assets/GGF_resized.mp4', 
                          state='play', 
                          options={'eos': 'loop'})
        layout.add_widget(self.video)
        
        # Control buttons
        btn_layout = BoxLayout(size_hint_y=0.1)
        
        play_btn = Button(text='Play')
        play_btn.bind(on_press=lambda x: setattr(self.video, 'state', 'play'))
        btn_layout.add_widget(play_btn)
        
        pause_btn = Button(text='Pause')
        pause_btn.bind(on_press=lambda x: setattr(self.video, 'state', 'pause'))
        btn_layout.add_widget(pause_btn)
        
        stop_btn = Button(text='Stop')
        stop_btn.bind(on_press=lambda x: setattr(self.video, 'state', 'stop'))
        btn_layout.add_widget(stop_btn)
        
        layout.add_widget(btn_layout)
        
        return layout

if __name__ == '__main__':
    print("Testing video playback...")
    print(f"Platform: {platform.system()}")
    print(f"SDL_AUDIODRIVER: {os.environ.get('SDL_AUDIODRIVER', 'not set')}")
    print(f"KIVY_AUDIO: {os.environ.get('KIVY_AUDIO', 'not set')}")
    VideoTestApp().run()
