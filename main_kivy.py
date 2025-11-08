"""
Kivy Frog Quiz App - Full Mobile & Web Compatible Version
Matches NiceGUI UI exactly, works as APK and web deployment
Uses full-size videos (_resized.mp4) for best quality
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from pathlib import Path
import random
import platform

# Force landscape
Window.size = (1600, 720)
Window.clearcolor = (0.18, 0.54, 0.34, 1)  # #2E8B57 green

# Frog data - using full-size _resized.mp4 videos
FROGS = [
    {"name": "Growling Grass\nFrog", "photo": "assets/GGF.png", "species": "Ranoidea (nee Litoria) raniformis",
     "video": "assets/GGF_resized.mp4", "preview": "assets/GGF_spec_safe3_preview.jpg", "id": "ggf"},
    {"name": "Southern Brown\nTree Frog", "photo": "assets/SBTF.png", "species": "Litoria ewingii", 
     "video": "assets/SBTF_resized.mp4", "preview": "assets/SBTF_spec_safe3_preview.jpg", "id": "sbtf"},
    {"name": "Peron's Tree\nFrog", "photo": "assets/PTF.png", "species": "Litoria peronii",
     "video": "assets/PTF_resized.mp4", "preview": "assets/PTF_spec_safe3_preview.jpg", "id": "ptf"},
    {"name": "Pobblebonk\nFrog", "photo": "assets/PBF.png", "species": "Limnodynastes dumerili",
     "video": "assets/PBF_resized.mp4", "preview": "assets/PBF_spec_safe3_preview.jpg", "id": "pbf"},
    {"name": "Common\nFroglet", "photo": "assets/CF.png", "species": "Crinia signifera",
     "video": "assets/CF_resized.mp4", "preview": "assets/CF_spec_safe3_preview.jpg", "id": "cf"},
    {"name": "Common Spadefoot\nToad", "photo": "assets/CSFT.png", "species": "Neobatrachus sudelli",
     "video": "assets/CSFT_resized.mp4", "preview": "assets/CSFT_spec_safe3_preview.jpg", "id": "csft"},
    {"name": "Eastern Sign-bearing\nFroglet", "photo": "assets/ESBF.png", "species": "Geocrinia victoriana",
     "video": "assets/ESBF_resized.mp4", "preview": "assets/ESBF_spec_safe3_preview.jpg", "id": "esbf"},
    {"name": "Spotted Marsh\nFrog", "photo": "assets/SMF.png", "species": "Limnodynastes tasmaniensis",
     "video": "assets/SMF_resized.mp4", "preview": "assets/SMF_spec_safe3_preview.jpg", "id": "smf"},
]


class RoundedButton(Button):
    """Custom button with rounded corners matching NiceGUI style"""
    pass


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
        
        # Load video - it will show first frame as thumbnail
        video_path = Path(frog['video']).absolute()
        if video_path.exists():
            print(f"Loading video: {video_path}")
            self.video.source = str(video_path)
            # Load the video but don't play - shows first frame
            self.video.state = 'pause'
            Clock.schedule_once(lambda dt: setattr(self.video, 'state', 'pause'), 0.1)
        else:
            print(f"Video not found: {video_path}")
        
        self.playing = False
        self.play_btn.background_normal = 'assets/PLAY.png'
    
    def toggle_video(self, instance):
        try:
            if self.playing:
                self.video.state = 'pause'
                self.play_btn.background_normal = 'assets/PLAY.png'
                self.playing = False
            else:
                self.video.state = 'play'
                self.play_btn.background_normal = 'assets/PAUSE.png'
                self.playing = True
        except Exception as e:
            print(f"Video playback error: {e}")
            # Video might not be loaded, just toggle button state
            self.playing = not self.playing
            self.play_btn.background_normal = 'assets/PAUSE.png' if self.playing else 'assets/PLAY.png'
    
    def go_home(self):
        try:
            self.video.state = 'stop'
        except:
            pass
        self.playing = False
        self.manager.go_to('home')
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


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
            text='🐸 Mystery Frog Quiz',
            size_hint=(1, 0.08),
            font_size='32sp',
            color=(0, 0.5, 0, 1),
            bold=True
        )
        content.add_widget(title)
        
        # Video
        self.video = Video(size_hint=(1, 0.5), state='stop', options={'eos': 'loop'})
        content.add_widget(self.video)
        
        # Bottom section
        bottom = BoxLayout(size_hint=(1, 0.42), spacing=20)
        
        # Left controls
        controls = BoxLayout(orientation='vertical', size_hint=(0.25, 1), spacing=15)
        
        back_btn = Button(background_normal='assets/Arrow.png', 
                         background_down='assets/Arrow.png')
        back_btn.bind(on_press=lambda x: self.go_home())
        controls.add_widget(back_btn)
        
        self.play_btn = Button(background_normal='assets/PLAY.png',
                              background_down='assets/PLAY.png')
        self.play_btn.bind(on_press=self.toggle_video)
        controls.add_widget(self.play_btn)
        
        bottom.add_widget(controls)
        
        # Right quiz area
        quiz_area = BoxLayout(orientation='vertical', size_hint=(0.75, 1), spacing=10)
        
        quiz_title = Label(text='Guess the Frog:', size_hint=(1, 0.12), 
                          font_size='24sp', color=(0, 0, 0, 1), bold=True)
        quiz_area.add_widget(quiz_title)
        
        # Answer grid
        self.answer_grid = GridLayout(cols=2, spacing=8, size_hint=(1, 0.6))
        quiz_area.add_widget(self.answer_grid)
        
        # Result
        self.result_lbl = Label(text='', size_hint=(1, 0.15), font_size='22sp', bold=True)
        quiz_area.add_widget(self.result_lbl)
        
        # Try again
        self.try_again_btn = Button(
            text='🔄 Try Again?',
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
    
    def on_enter(self):
        self.new_quiz()
    
    def new_quiz(self):
        self.current_frog = random.choice(FROGS)
        self.revealed = False
        self.playing = False
        
        # Set video
        video_path = Path(self.current_frog['video'])
        if not video_path.exists():
            fallback = self.current_frog['video'].replace('_mobile.mp4', '_resized.mp4')
            self.video.source = fallback
        else:
            self.video.source = self.current_frog['video']
        
        self.video.state = 'stop'
        self.play_btn.background_normal = 'assets/PLAY.png'
        self.result_lbl.text = ''
        self.try_again_btn.opacity = 0
        
        # Generate answers
        self.answer_grid.clear_widgets()
        options = random.sample([f for f in FROGS if f != self.current_frog], k=min(3, len(FROGS) - 1))
        options.append(self.current_frog)
        random.shuffle(options)
        
        for frog in options:
            btn = Button(
                text=frog['name'],
                background_color=(0.3, 0.69, 0.31, 1),
                font_size='18sp'
            )
            btn.bind(on_press=lambda x, f=frog: self.check_answer(f))
            self.answer_grid.add_widget(btn)
    
    def check_answer(self, selected):
        if self.revealed:
            return
        self.revealed = True
        self.try_again_btn.opacity = 1
        
        if selected == self.current_frog:
            self.result_lbl.text = f"✅ Correct! It's the {self.current_frog['name'].replace(chr(10), ' ')}"
            self.result_lbl.color = (0, 0.7, 0, 1)
        else:
            self.result_lbl.text = f"❌ Oops! It was the {self.current_frog['name'].replace(chr(10), ' ')}"
            self.result_lbl.color = (1, 0, 0, 1)
    
    def toggle_video(self, instance):
        if self.playing:
            self.video.state = 'pause'
            self.play_btn.background_normal = 'assets/PLAY.png'
            self.playing = False
        else:
            self.video.state = 'play'
            self.play_btn.background_normal = 'assets/PAUSE.png'
            self.playing = True
    
    def go_home(self):
        self.video.state = 'stop'
        self.playing = False
        self.manager.go_to('home')
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class AppInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main = FloatLayout()
        with main.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=main.size, pos=main.pos)
        main.bind(size=self._update_rect, pos=self._update_rect)
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(text='App Info', size_hint=(1, 0.1), font_size='36sp', color=(0, 0, 0, 1), bold=True)
        content.add_widget(title)
        
        info = Label(
            text='This app was created and designed by Katie Howard\n'
                 'for the exhibition "Litoria\'s Wetland World".\n\n'
                 'Sound files provided by Arthur Rylah Institute\n'
                 'Spectrograms created using PASE',
            size_hint=(1, 0.7),
            font_size='22sp',
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        info.bind(size=info.setter('text_size'))
        content.add_widget(info)
        
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


class FrogScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = SlideTransition(duration=0.3)
        
        self.add_widget(HomeScreen(name='home'))
        self.add_widget(FrogDetailScreen(name='frog'))
        self.add_widget(InstructionsScreen(name='instructions'))
        self.add_widget(MysteryScreen(name='mystery'))
        self.add_widget(AppInfoScreen(name='app_info'))
        
        self.current = 'home'
    
    def show_frog(self, frog):
        self.get_screen('frog').set_frog(frog)
        self.current = 'frog'
    
    def go_to(self, screen_name):
        self.current = screen_name


class FrogQuizApp(App):
    def build(self):
        return FrogScreenManager()


if __name__ == '__main__':
    FrogQuizApp().run()
