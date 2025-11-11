"""Frog detail screen with video spectrogram"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.uix.widget import Widget
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
        header.add_widget(Widget(size_hint=(0.15, 1)))  # Left spacer
        self.name_lbl = Label(font_size='32sp', color=(0, 0, 0, 1), bold=True, 
                             size_hint=(0.35, 1), halign='center', valign='middle',
                             text_size=(None, None), max_lines=2)
        self.name_lbl.bind(width=lambda l, w: setattr(l, 'text_size', (w - 10, None)))
        self.species_lbl = Label(font_size='26sp', color=(0, 0, 0, 1), italic=True,
                                size_hint=(0.35, 1), halign='center', valign='middle',
                                text_size=(None, None), max_lines=2)
        self.species_lbl.bind(width=lambda l, w: setattr(l, 'text_size', (w - 10, None)))
        header.add_widget(self.name_lbl)
        header.add_widget(self.species_lbl)
        header.add_widget(Widget(size_hint=(0.15, 1)))  # Right spacer
        content.add_widget(header)
        
        # Video with preview thumbnail - stop after playing once (no loop)
        video_options = {'eos': 'stop'}  # Stop at end of stream instead of looping
        self.video = Video(size_hint=(1, 0.65), state='stop', options=video_options)
        self.video.bind(state=self._on_video_state_change)  # Monitor video state changes
        content.add_widget(self.video)
        
        # Controls
        controls = BoxLayout(size_hint=(1, 0.25), spacing=40, padding=[50, 10])
        
        # Play button - maintain square aspect
        play_container = BoxLayout(size_hint=(0.2, 1))
        self.play_btn = Button(background_normal='assets/PLAY.png', 
                               background_down='assets/PLAY.png',
                               size_hint=(None, None))
        self.play_btn.bind(on_press=self.toggle_video)
        play_container.bind(size=lambda i, v: self._update_button_size(self.play_btn, i))
        play_container.add_widget(self.play_btn)
        controls.add_widget(play_container)
        
        # Frog photo
        self.frog_img = Image(size_hint=(0.3, 1))
        controls.add_widget(self.frog_img)
        
        # Back button - maintain square aspect
        back_container = BoxLayout(size_hint=(0.2, 1))
        back_btn = Button(background_normal='assets/Arrow.png',
                         background_down='assets/Arrow.png',
                         size_hint=(None, None))
        back_btn.bind(on_press=lambda x: self.go_home())
        back_container.bind(size=lambda i, v: self._update_button_size(back_btn, i))
        back_container.add_widget(back_btn)
        controls.add_widget(back_container)
        
        content.add_widget(controls)
        main.add_widget(content)
        self.add_widget(main)
    
    def _update_button_size(self, button, container):
        """Maintain square aspect ratio for buttons"""
        if container.width > 0 and container.height > 0:
            size = min(container.width, container.height)
            button.size = (size, size)
    
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
    
    def _on_video_state_change(self, instance, value):
        """Handle video state changes - update play button when video stops"""
        if value == 'stop':
            self.playing = False
            self.play_btn.background_normal = 'assets/PLAY.png'
            print("Video stopped - resetting play button")
    
    def _load_video(self, video_file):
        """Load video with proper path handling and show first frame"""
        try:
            # Use relative path for Android, absolute for desktop
            if platform.system() == 'Android' or 'ANDROID_ARGUMENT' in os.environ:
                video_path = video_file
            else:
                # For desktop, make sure path is relative to the script location
                script_dir = Path(__file__).parent.parent
                video_path = str(script_dir / video_file)
            
            print(f"Loading video: {video_path}")
            
            # Check if file exists
            if os.path.exists(video_path):
                print(f"✓ Video file found: {video_path}")
            else:
                print(f"✗ Video file NOT found: {video_path}")
            
            # Set video source
            self.video.source = video_path
            
            # Workaround for Kivy video thumbnail issue #7755
            # Need to play the video briefly to load first frame, then pause
            self.video.state = 'play'
            self.video.volume = 0  # Mute during thumbnail load
            
            # Schedule pause after video has time to load first frame
            Clock.schedule_once(lambda dt: self._pause_at_first_frame(), 0.3)
            
        except Exception as e:
            print(f"Error loading video: {e}")
    
    def _pause_at_first_frame(self):
        """Pause video after first frame loads to show thumbnail"""
        try:
            # Seek to start and pause to show first frame
            if hasattr(self.video, 'seek'):
                self.video.seek(0)
            self.video.state = 'pause'
            self.video.volume = 1.0  # Restore volume for playback
            print("Video paused at first frame")
        except Exception as e:
            print(f"Error pausing video: {e}")
    
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
