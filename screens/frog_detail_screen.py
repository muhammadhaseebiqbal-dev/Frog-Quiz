"""Frog detail screen with video spectrogram"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from pathlib import Path
import platform
import os


class FrogDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_frog = None
        self.playing = False
        
        main = FloatLayout()
        with main.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=main.size, pos=main.pos)
        main.bind(size=self._update_rect, pos=self._update_rect)
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.name_lbl = Label(font_size='28sp', color=(0, 0, 0, 1), bold=True)
        self.species_lbl = Label(font_size='24sp', color=(0, 0, 0, 1), italic=True)
        header.add_widget(self.name_lbl)
        header.add_widget(self.species_lbl)
        content.add_widget(header)
        
        # Video with preview thumbnail
        self.video = Video(size_hint=(1, 0.65), state='stop', options={'eos': 'loop'})
        content.add_widget(self.video)
        
        # Controls
        controls = BoxLayout(size_hint=(1, 0.25), spacing=40, padding=[50, 10])
        
        # Play button
        self.play_btn = Button(background_normal='assets/PLAY.png', 
                               background_down='assets/PLAY.png',
                               size_hint=(0.2, 1))
        self.play_btn.bind(on_press=self.toggle_video)
        controls.add_widget(self.play_btn)
        
        # Frog photo
        self.frog_img = Image(size_hint=(0.3, 1))
        controls.add_widget(self.frog_img)
        
        # Back button
        back_btn = Button(background_normal='assets/Arrow.png',
                         background_down='assets/Arrow.png',
                         size_hint=(0.2, 1))
        back_btn.bind(on_press=lambda x: self.go_home())
        controls.add_widget(back_btn)
        
        content.add_widget(controls)
        main.add_widget(content)
        self.add_widget(main)
    
    def set_frog(self, frog):
        self.current_frog = frog
        self.name_lbl.text = frog['name'].replace('\n', ' ')
        self.species_lbl.text = frog['species']
        self.frog_img.source = frog['photo']
        
        # Stop and cleanup any currently playing video first
        try:
            if self.video.state != 'stop':
                self.video.state = 'stop'
            self.video.unload()
            # Give video time to cleanup
            Clock.schedule_once(lambda dt: self._load_video(frog['video']), 0.2)
        except Exception as e:
            print(f"Error stopping video: {e}")
            self._load_video(frog['video'])
        
        self.playing = False
        self.play_btn.background_normal = 'assets/PLAY.png'
    
    def _load_video(self, video_file):
        """Load video with proper path handling"""
        try:
            # Use relative path for Android, absolute for desktop
            if platform.system() == 'Android' or 'ANDROID_ARGUMENT' in os.environ:
                video_path = video_file
            else:
                video_path = str(Path(video_file).absolute())
            
            print(f"Loading video: {video_path}")
            
            # Check if file exists
            if os.path.exists(video_path):
                print(f"✓ Video file found: {video_path}")
            else:
                print(f"✗ Video file NOT found: {video_path}")
            
            # Set video source (don't play yet)
            self.video.source = video_path
            self.video.state = 'stop'
            
        except Exception as e:
            print(f"Error loading video: {e}")
    
    def toggle_video(self, instance):
        """Toggle video playback with improved error handling"""
        if not self.current_frog:
            return
            
        try:
            if self.playing:
                # Pause video
                self.video.state = 'pause'
                self.play_btn.background_normal = 'assets/PLAY.png'
                self.playing = False
                print("Video paused")
            else:
                # Play video
                if self.video.state == 'stop':
                    # Video needs to be loaded first
                    print("Starting video playback...")
                    self.video.state = 'play'
                    # Give it a moment to initialize
                    Clock.schedule_once(lambda dt: self._ensure_playing(), 0.3)
                else:
                    self.video.state = 'play'
                    print("Resuming video playback")
                    
                self.play_btn.background_normal = 'assets/PAUSE.png'
                self.playing = True
                
        except Exception as e:
            print(f"Video playback error: {e}")
            # Reset state on error
            self.playing = False
            self.play_btn.background_normal = 'assets/PLAY.png'
    
    def _ensure_playing(self):
        """Ensure video is actually playing"""
        try:
            if self.playing and self.video.state != 'play':
                print("Force setting video to play state")
                self.video.state = 'play'
        except Exception as e:
            print(f"Error ensuring playback: {e}")
    
    def go_home(self):
        """Return to home screen and cleanup video"""
        try:
            if self.video.state != 'stop':
                self.video.state = 'stop'
            # Schedule unload to prevent crashes
            Clock.schedule_once(lambda dt: self.video.unload(), 0.1)
        except Exception as e:
            print(f"Error stopping video: {e}")
        
        self.playing = False
        self.play_btn.background_normal = 'assets/PLAY.png'
        self.manager.go_to('home')
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
