"""Lazy loading screen manager for improved startup performance"""
import json
import importlib
from kivy.uix.screenmanager import ScreenManager, SlideTransition


class LazyScreenManager(ScreenManager):
    """
    Screen manager that loads screens on-demand for faster startup.
    Screens are only imported and instantiated when first navigated to.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = SlideTransition(duration=0.3)
        
        # Load screen registry from JSON
        with open('screens.json', 'r') as f:
            self.screen_registry = json.load(f)
        
        # Track which screens have been loaded
        self.loaded_screens = set()
    
    def load_screen(self, screen_name):
        """
        Dynamically load a screen if it hasn't been loaded yet.
        
        Args:
            screen_name: Name of the screen to load (from screens.json)
        """
        # Skip if already loaded
        if screen_name in self.loaded_screens:
            return
        
        # Get screen configuration
        if screen_name not in self.screen_registry:
            print(f"Warning: Screen '{screen_name}' not found in registry")
            return
        
        screen_config = self.screen_registry[screen_name]
        
        try:
            # Dynamically import the module
            print(f"Loading screen: {screen_name}")
            module = importlib.import_module(screen_config['module'])
            
            # Get the screen class
            screen_class = getattr(module, screen_config['class'])
            
            # Instantiate and add to manager
            screen_instance = screen_class(name=screen_name)
            self.add_widget(screen_instance)
            
            # Mark as loaded
            self.loaded_screens.add(screen_name)
            print(f"✓ Screen '{screen_name}' loaded successfully")
            
        except Exception as e:
            print(f"✗ Error loading screen '{screen_name}': {e}")
            import traceback
            traceback.print_exc()
    
    def go_to(self, screen_name):
        """
        Navigate to a screen, loading it first if needed.
        
        Args:
            screen_name: Name of the screen to navigate to
        """
        # Load screen if not already loaded
        self.load_screen(screen_name)
        
        # Switch to the screen
        if self.has_screen(screen_name):
            self.current = screen_name
        else:
            print(f"Warning: Could not navigate to '{screen_name}'")
    
    def show_frog(self, frog):
        """
        Load frog detail screen and pass frog data.
        
        Args:
            frog: Dictionary containing frog data
        """
        # Load screen if needed
        self.load_screen('frog')
        
        # Pass frog data to screen
        if self.has_screen('frog'):
            self.get_screen('frog').set_frog(frog)
            self.current = 'frog'
