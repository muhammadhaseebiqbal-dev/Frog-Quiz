"""Mystery frog quiz screen"""
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from screens.frog_data import FROGS
from pathlib import Path
import random
import platform
import os


class MysteryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_frog = None
        self.revealed = False
        self.playing = False
        
        main = FloatLayout()
        with main.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=main.size, pos=main.pos)
        main.bind(size=self._update_rect, pos=self._update_rect)
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text='Mystery Frog Quiz',
            size_hint=(1, 0.08),
            font_size='32sp',
            color=(0, 0.5, 0, 1),
            bold=True
        )
        content.add_widget(title)
        
        # Video - stop after playing once (no loop)
        video_options = {'eos': 'stop'}  # Stop at end of stream instead of looping
        self.video = Video(size_hint=(1, 0.5), state='stop', options=video_options)
        self.video.bind(state=self._on_video_state_change)  # Monitor video state changes
        content.add_widget(self.video)
        
        # Bottom section
        bottom = BoxLayout(size_hint=(1, 0.42), spacing=20)
        
        # Left controls
        controls = BoxLayout(orientation='vertical', size_hint=(0.25, 1), spacing=15)
        
        # Back button - maintain square aspect
        back_container = BoxLayout(size_hint=(1, 0.5))
        back_btn = Button(background_normal='assets/Arrow.png', 
                         background_down='assets/Arrow.png',
                         size_hint=(None, None))
        back_btn.bind(on_press=lambda x: self.go_home())
        back_container.bind(size=lambda i, v: self._update_button_size(back_btn, i))
        back_container.add_widget(back_btn)
        controls.add_widget(back_container)
        
        # Play button - maintain square aspect
        play_container = BoxLayout(size_hint=(1, 0.5))
        self.play_btn = Button(background_normal='assets/PLAY.png',
                              background_down='assets/PLAY.png',
                              size_hint=(None, None))
        self.play_btn.bind(on_press=self.toggle_video)
        play_container.bind(size=lambda i, v: self._update_button_size(self.play_btn, i))
        play_container.add_widget(self.play_btn)
        controls.add_widget(play_container)
        
        bottom.add_widget(controls)
        
        # Right quiz area
        quiz_area = BoxLayout(orientation='vertical', size_hint=(0.75, 1), spacing=10)
        
        quiz_title = Label(text='Guess the Frog:', size_hint=(1, 0.12), 
                          font_size='24sp', color=(0, 0, 0, 1), bold=True)
        quiz_area.add_widget(quiz_title)
        
        # Answer grid - 4 columns for all 8 frogs
        self.answer_grid = GridLayout(cols=4, spacing=8, size_hint=(1, 0.6))
        quiz_area.add_widget(self.answer_grid)
        
        # Result
        self.result_lbl = Label(text='', size_hint=(1, 0.15), font_size='22sp', bold=True)
        quiz_area.add_widget(self.result_lbl)
        
        # Try again
        self.try_again_btn = Button(
            text='Try Again?',
            size_hint=(1, 0.13),
            background_color=(1, 0.84, 0, 1),
            font_size='20sp',
            opacity=0
        )
        self.try_again_btn.bind(on_press=lambda x: self.new_quiz())
        quiz_area.add_widget(self.try_again_btn)
        
        bottom.add_widget(quiz_area)
        content.add_widget(bottom)
        
        main.add_widget(content)
        self.add_widget(main)
    
    def _update_button_size(self, button, container):
        """Maintain square aspect ratio for buttons"""
        if container.width > 0 and container.height > 0:
            size = min(container.width, container.height)
            button.size = (size, size)
    
    def on_enter(self):
        self.new_quiz()
    
    def new_quiz(self):
        self.current_frog = random.choice(FROGS)
        self.revealed = False
        self.playing = False
        
        # Stop and cleanup any currently playing video first
        try:
            if self.video.state != 'stop':
                self.video.state = 'stop'
            self.video.unload()
            # Give video time to cleanup before loading new one
            Clock.schedule_once(lambda dt: self._load_quiz_video(), 0.2)
        except Exception as e:
            print(f"Error stopping quiz video: {e}")
            self._load_quiz_video()
        
        self.play_btn.background_normal = 'assets/PLAY.png'
        self.result_lbl.text = ''
        self.try_again_btn.opacity = 0
        
        # Generate answers
        self.answer_grid.clear_widgets()
        options = random.sample([f for f in FROGS if f != self.current_frog], k=min(7, len(FROGS) - 1))
        options.append(self.current_frog)
        random.shuffle(options)
        
        for frog in options:
            btn = Button(
                text=frog['name'],
                background_color=(0.3, 0.69, 0.31, 1),
                background_normal='',  # Required for background_color to work
                font_size='20sp',
                text_size=(None, None),
                halign='center',
                valign='middle',
                padding=(5, 5)
            )
            btn.bind(width=lambda b, w: setattr(b, 'text_size', (w - 10, None)))
            btn.frog_data = frog  # Store frog reference on button
            btn.bind(on_press=lambda x, f=frog: self.check_answer(f))
            self.answer_grid.add_widget(btn)
    
    def _on_video_state_change(self, instance, value):
        """Handle video state changes - update play button when video stops"""
        if value == 'stop':
            self.playing = False
            self.play_btn.background_normal = 'assets/PLAY.png'
            print("Quiz video stopped - resetting play button")
    
    def _load_quiz_video(self):
        """Load quiz video with proper path handling and show first frame"""
        try:
            # Use relative path for Android, absolute for desktop
            if platform.system() == 'Android' or 'ANDROID_ARGUMENT' in os.environ:
                video_path = self.current_frog['video']
            else:
                # For desktop, make sure path is relative to the script location
                script_dir = Path(__file__).parent.parent
                video_path = str(script_dir / self.current_frog['video'])
            
            print(f"Loading quiz video: {video_path}")
            
            # Set video source
            self.video.source = video_path
            
            # Workaround for Kivy video thumbnail issue #7755
            # Need to play the video briefly to load first frame, then pause
            self.video.state = 'play'
            self.video.volume = 0  # Mute during thumbnail load
            
            # Schedule pause after video has time to load first frame
            Clock.schedule_once(lambda dt: self._pause_quiz_at_first_frame(), 0.3)
            
        except Exception as e:
            print(f"Error loading quiz video: {e}")
    
    def _pause_quiz_at_first_frame(self):
        """Pause quiz video after first frame loads to show thumbnail"""
        try:
            # Seek to start and pause to show first frame
            if hasattr(self.video, 'seek'):
                self.video.seek(0)
            self.video.state = 'pause'
            self.video.volume = 1.0  # Restore volume for playback
            print("Quiz video paused at first frame")
        except Exception as e:
            print(f"Error pausing quiz video: {e}")
    
    def check_answer(self, selected):
        if self.revealed:
            return
        self.revealed = True
        self.try_again_btn.opacity = 1
        
        # Visual feedback for all buttons
        for child in self.answer_grid.children:
            if isinstance(child, Button):
                frog_data = getattr(child, 'frog_data', None)
                
                if frog_data == selected:
                    # Selected answer gets black border
                    from kivy.graphics import Color, Line
                    with child.canvas.after:
                        Color(0, 0, 0, 1)  # Black
                        Line(rectangle=(child.x, child.y, child.width, child.height), width=3)
                
                if frog_data == self.current_frog:
                    # Correct answer gets yellow/gold background
                    child.background_color = (1, 0.84, 0, 1)  # Gold/yellow
                elif frog_data != selected:
                    # Other incorrect answers fade out
                    child.background_color = (0.3, 0.69, 0.31, 0.3)  # Faded green
        
        # Update result text
        if selected == self.current_frog:
            self.result_lbl.text = f"CORRECT! It's the {self.current_frog['name'].replace(chr(10), ' ')}"
            self.result_lbl.color = (0, 0.7, 0, 1)
        else:
            self.result_lbl.text = f"Oops! It was the {self.current_frog['name'].replace(chr(10), ' ')}"
            self.result_lbl.color = (1, 0, 0, 1)
    
    def toggle_video(self, instance):
        """Toggle quiz video playback with improved error handling"""
        if not self.current_frog:
            return
            
        try:
            if self.playing:
                # Pause video
                self.video.state = 'pause'
                self.play_btn.background_normal = 'assets/PLAY.png'
                self.playing = False
                print("Quiz video paused")
            else:
                # Play video
                if self.video.state == 'stop':
                    print("Starting quiz video playback...")
                    self.video.state = 'play'
                    # Give it a moment to initialize
                    Clock.schedule_once(lambda dt: self._ensure_quiz_playing(), 0.3)
                else:
                    self.video.state = 'play'
                    print("Resuming quiz video playback")
                    
                self.play_btn.background_normal = 'assets/PAUSE.png'
                self.playing = True
                
        except Exception as e:
            print(f"Quiz video playback error: {e}")
            self.playing = False
            self.play_btn.background_normal = 'assets/PLAY.png'
    
    def _ensure_quiz_playing(self):
        """Ensure quiz video is actually playing"""
        try:
            if self.playing and self.video.state != 'play':
                print("Force setting quiz video to play state")
                self.video.state = 'play'
        except Exception as e:
            print(f"Error ensuring quiz playback: {e}")
    
    def go_home(self):
        """Return to home screen and cleanup quiz video"""
        try:
            if self.video.state != 'stop':
                self.video.state = 'stop'
            # Schedule unload to prevent crashes
            Clock.schedule_once(lambda dt: self.video.unload(), 0.1)
        except Exception as e:
            print(f"Error stopping quiz video: {e}")
        
        self.playing = False
        self.play_btn.background_normal = 'assets/PLAY.png'
        self.manager.go_to('home')
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
