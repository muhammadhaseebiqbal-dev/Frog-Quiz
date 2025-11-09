"""
Kivy Frog Quiz App - Full Mobile & Web Compatible Version with Lazy Loading
Matches NiceGUI UI exactly, works as APK and web deployment
Uses full-size videos (_resized.mp4) for best quality

PERFORMANCE OPTIMIZATION:
- Screens are loaded on-demand (lazy loading) for faster startup
- Only the home screen is loaded initially
- Other screens load when first navigated to
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from lazy_manager import LazyScreenManager
import platform
import os

# Configure Kivy audio for proper video playback
os.environ['KIVY_AUDIO'] = 'sdl2'  # Use SDL2 audio

# Platform-specific audio driver configuration
if platform.system() == 'Android' or 'ANDROID_ARGUMENT' in os.environ:
    # Android: Use OpenSL ES instead of AAudio (prevents crashes)
    os.environ['SDL_AUDIODRIVER'] = 'opensles'
elif platform.system() == 'Windows':
    # Windows: Use default DirectSound driver
    os.environ['SDL_AUDIODRIVER'] = 'directsound'
elif platform.system() == 'Darwin':  # macOS
    # macOS: Use default CoreAudio driver
    os.environ['SDL_AUDIODRIVER'] = 'coreaudio'
else:
    # Linux: Use ALSA or PulseAudio (SDL will auto-detect)
    os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'

# Force landscape orientation on desktop (Android handles this via buildozer.spec)
if platform.system() not in ['Android', 'Linux']:  # Don't set size on Android
    Window.size = (1600, 720)
Window.clearcolor = (0.18, 0.54, 0.34, 1)  # #2E8B57 green


# Force landscape orientation on desktop (Android handles this via buildozer.spec)
if platform.system() not in ['Android', 'Linux']:  # Don't set size on Android
    Window.size = (1600, 720)
Window.clearcolor = (0.18, 0.54, 0.34, 1)  # #2E8B57 green


class FrogQuizApp(App):
    """
    Main Kivy application with lazy loading for fast startup.
    Only loads home screen initially, other screens load on-demand.
    """
    
    def build(self):
        """Build app and load only the home screen"""
        # Create lazy loading screen manager
        sm = LazyScreenManager()
        
        # Load only the home screen initially (fast startup!)
        sm.load_screen('home')
        sm.current = 'home'
        
        # Force UI refresh after launch to fix blank screen issue on Android
        Clock.schedule_once(lambda dt: self._force_refresh(sm), 0.5)
        
        return sm
    
    def _force_refresh(self, sm):
        """Force a screen refresh to fix blank screen on Android launch"""
        try:
            current_screen = sm.current
            # Trigger a layout update by briefly switching screens
            sm.current = 'home'
            if current_screen != 'home':
                Clock.schedule_once(lambda dt: setattr(sm, 'current', current_screen), 0.1)
        except:
            pass


if __name__ == '__main__':
    FrogQuizApp().run()

