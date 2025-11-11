from nicegui import ui, app
from datetime import datetime
from pathlib import Path
import random
import platform
import os
import json


## local assets folder
app.add_static_files('/assets', Path(__file__).parent / 'assets')

## Serve manifest.json via custom route
@app.get('/manifest.json')
async def serve_manifest():
    manifest_path = Path(__file__).parent / 'manifest.json'
    with open(manifest_path, 'r') as f:
        return json.load(f)

## def helper function 
def resource_path(rel_path: str) -> str:
    # return proper URL path for assets
    if rel_path.startswith('assets/'):
        rel_path = rel_path.replace('assets/', '', 1)
    return f'/assets/{rel_path}'


## Frog data 
frogs_list = [
        {"name": "Growling Grass \nFrog", "photo": "/assets/GGF.png", "Species name": "Ranoidea (nee Litoria) raniformis",
        "video": "/assets/GGF_resized.mp4", "preview": "/assets/GGF_spec_safe3_preview.jpg",
        "ind_name": "Growling Grass Frog"},
        {"name": "Southern Brown \nTree Frog", "photo": "/assets/SBTF.png", "Species name": "Litoria ewingii", 
        "video": "/assets/SBTF_resized.mp4", "preview":"/assets/SBTF_spec_safe3_preview.jpg",
        "ind_name": "Southern Brown Tree Frog"},
        {"name": "Peron's Tree \nFrog", "photo": "/assets/PTF.png", "Species name": "Litoria peronii",
        "video": "/assets/PTF_resized.mp4", "preview": "/assets/PTF_spec_safe3_preview.jpg",
        "ind_name": "Peron's Tree Frog"},
        {"name": "Pobblebonk \nFrog", "photo": "/assets/PBF.png", "Species name": "Limnodynastes dumerili",
        "video": "/assets/PBF_resized.mp4", "preview": "/assets/PBF_spec_safe3_preview.jpg",
        "ind_name": "Pobblebonk Frog"},
        {"name": "Common \nFroglet", "photo": "/assets/CF.png", "Species name": "Crinia signifera",
        "video": "/assets/CF_resized.mp4", "preview": "/assets/CF_spec_safe3_preview.jpg",
        "ind_name": "Common Froglet"},
        {"name": "Common Spadefoot \nToad", "photo": "/assets/CSFT.png", "Species name": "Neobatrachus sudelli",
        "video": "/assets/CSFT_resized.mp4", "preview": "/assets/CSFT_spec_safe3_preview.jpg",
        "ind_name": "Sudell's Frog"},
        {"name": "Eastern Sign-bearing \nFroglet", "photo": "/assets/ESBF.png", "Species name" : "Geocrinia victoriana",
        "video": "/assets/ESBF_resized.mp4", "preview": "/assets/ESBF_spec_safe3_preview.jpg",
        "ind_name": "Eastern Sign-bearing Froglet"},
        {"name": "Spotted Marsh \nFrog", "photo": "/assets/SMF.png", "Species name" : "Limnodynastes tasmaniensis",
        "video": "/assets/SMF_resized.mp4", "preview": "/assets/SMF_spec_safe3_preview.jpg",
        "ind_name": "Spotted Marsh Frog"},
    ]


# --- Home page ---
@ui.page('/')
def home_page():  
    # Add PWA meta tags for mobile
    ui.add_head_html('''
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="theme-color" content="#2E8B57">
        <link rel="manifest" href="/manifest.json">
        <link rel="apple-touch-icon" href="/assets/UnknownFrog.png">
    ''')
    
    # Add fullscreen functionality - triggers silently on first user interaction
    ui.add_head_html('''
        <script>
        let fullscreenRequested = false;
        
        function triggerFullscreen(e) {
            if (!fullscreenRequested && e && e.isTrusted) {
                fullscreenRequested = true;
                
                const elem = document.documentElement;
                if (elem.requestFullscreen) {
                    elem.requestFullscreen().catch(() => {
                        fullscreenRequested = false;
                    });
                } else if (elem.webkitRequestFullscreen) {
                    elem.webkitRequestFullscreen();
                } else if (elem.mozRequestFullScreen) {
                    elem.mozRequestFullScreen();
                } else if (elem.msRequestFullScreen) {
                    elem.msRequestFullScreen();
                }
                
                // Remove listeners after first attempt
                document.removeEventListener('click', triggerFullscreen);
                document.removeEventListener('touchstart', triggerFullscreen);
                document.removeEventListener('mousedown', triggerFullscreen);
                document.removeEventListener('keydown', triggerFullscreen);
            }
        }
        
        // Setup listeners on page load
        window.addEventListener('load', function() {
            document.addEventListener('click', triggerFullscreen);
            document.addEventListener('touchstart', triggerFullscreen);
            document.addEventListener('mousedown', triggerFullscreen);
            document.addEventListener('keydown', triggerFullscreen);
        });
        </script>
    ''')

    # ✅ Set the background color for the whole page
    ui.query('body').classes('bg-green-700')  # Tailwind green
    ui.query('body').style('background-color: #2E8B57;')  # fallback if classes don't apply

    # ✅ Title label - Responsive font size
    with ui.row().classes("justify-center items-center w-full px-4"):
        ui.label('Select a frog to see and hear its call').classes(
            'text-xl sm:text-2xl md:text-3xl lg:text-4xl text-center text-white my-4'
        )

    # ✅ Responsive grid layout - 1 col for screens < 800px, 5 cols for larger screens
    with ui.grid(columns=5).classes(
        'grid-cols-1 md:grid-cols-5 '
        'gap-4 sm:gap-6 w-full px-4 py-4 max-w-7xl mx-auto justify-items-center'
    ):
        with ui.column().classes('items-center gap-2 w-full max-w-xs'):
            with ui.button(color='transparent', on_click=lambda: ui.navigate.to('/instructions')).classes(
                'p-0 border-none w-full aspect-square max-w-[250px]'
            ):
                ui.image('/assets/App_overview.png').classes(
                    'w-full h-full object-cover rounded-2xl shadow-lg'
                )
            ui.label("How spectrograms show sound").classes(
                'text-base sm:text-lg md:text-xl lg:text-2xl font-medium text-center text-white'
            )     
        for frog in frogs_list:
            with ui.column().classes('items-center gap-2 w-full max-w-xs'):  
                # Button only contains the image
                with ui.button(
                    color='transparent',
                    on_click=lambda f=frog: ui.navigate.to(f'/frog/{f["ind_name"]}')
                ).classes('p-0 border-none w-full aspect-square max-w-[250px]'):
                    ui.image(frog['photo']).classes(
                        'w-full h-full object-cover rounded-2xl shadow-lg'
                    )
                    
                # Label below the button
                ui.label(frog['name']).classes(
                    'text-base sm:text-lg md:text-xl lg:text-2xl font-medium text-center text-white'
                )
            
        with ui.column().classes('items-center gap-2 w-full max-w-xs'):
            with ui.button(color='transparent', on_click=lambda: ui.navigate.to('/mystery')).classes(
                'p-0 border-none w-full aspect-square max-w-[250px]'
            ):
                ui.image('/assets/UnknownFrog.png').classes(
                    'w-full h-full object-cover rounded-2xl shadow-lg'
                )
            ui.label("Mystery Frog").classes(
                'text-base sm:text-lg md:text-xl lg:text-2xl font-medium text-center text-white'
            )     
      
                    

    # ✅ App info button at bottom - centered and responsive
    with ui.row().classes('w-full justify-center mt-4 px-4'):
        ui.button('App Info', on_click=lambda: ui.navigate.to('/app_info')).props('raised').classes(
            'bg-green-600 text-white text-lg sm:text-xl px-6 py-3 rounded-lg shadow-md hover:bg-green-700'
        )

    # ✅ Invisible triple-tap exit (top-left corner)
    exit_state = {"taps": 0, "last_tap": None}

    def triple_tap_exit(e):
        now = datetime.now()
        if exit_state["last_tap"] and (now - exit_state["last_tap"]).total_seconds() > 1:
            exit_state["taps"] = 0
        exit_state["taps"] += 1
        exit_state["last_tap"] = now
        if exit_state["taps"] >= 3:
            ui.notify('Exiting app...')
            app.shutdown()

    ui.button('', on_click=triple_tap_exit).style(
        'position: fixed; top:0px; left:0px; width:80px; height:80px; opacity:0;'
    )


#####################################
# --- Instructions page ---
@ui.page('/instructions')
def instructions_page():

    # Request fullscreen on user interaction
    ui.add_head_html('''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            function tryFullscreen(e) {
                if (e.isTrusted) {
                    const elem = document.documentElement;
                    if (elem.requestFullscreen) {
                        elem.requestFullscreen().catch(err => console.log('Fullscreen:', err.message));
                    } else if (elem.webkitRequestFullscreen) {
                        elem.webkitRequestFullscreen();
                    }
                    document.removeEventListener('click', tryFullscreen);
                }
            }
            if (!document.fullscreenElement && !document.webkitFullscreenElement) {
                document.addEventListener('click', tryFullscreen, { once: true });
            }
        });
        </script>
    ''')

    # 🌿 Background (optional, to match your theme)
    #ui.query('body').style('background-color: #2E8B57; color: white;')

    with ui.column().classes("w-full min-h-screen items-center justify-start bg-white px-4 py-6"):
        # --- Header ---
        with ui.row().classes("items-center justify-center w-full mb-4"):
            ui.label('Spectrograms display the frequency and amplitude of sound').classes(
                'text-xl sm:text-2xl md:text-3xl text-center font-bold text-green-800'
            )

        # --- Top Info Boxes (Two side-by-side on desktop, stacked on mobile) ---
        with ui.row().classes('justify-center gap-4 sm:gap-8 md:gap-12 lg:gap-20 mb-6 flex-wrap w-full'):
            ui.html("""
                <div style="font-size: 18px; max-width: 500px; text-align: left;">
                    Sounds are vibrations and the number of vibrations per second
                    determines the <b>frequency</b> or pitch of a sound.<br>
                    <b>Low pitch:</b> drum roll, growl<br>
                    <b>High pitch:</b> whistle, jingling keys
                </div>
            """, sanitize=False).classes('text-sm sm:text-base md:text-lg lg:text-xl')
            ui.html("""
                <div style="font-size: 18px; max-width: 500px; text-align: left;">
                    The size of sound waves determines <b>amplitude</b> — the larger the wave, the louder the sound.<br>
                    <b>Low amplitude:</b> whispering<br>
                    <b>High amplitude:</b> yelling
                </div>
            """, sanitize=False).classes('text-sm sm:text-base md:text-lg lg:text-xl')

        # --- Middle Image - Responsive ---
        ui.image('/assets/example.png').classes(
            "w-full max-w-5xl h-auto rounded-xl shadow-md border border-gray-300 mb-6"
        )

        # --- Bottom Row: Back Button + 2 Text Boxes (stacked on mobile) ---
        with ui.row().classes('justify-center items-center gap-4 sm:gap-8 md:gap-12 lg:gap-20 flex-wrap w-full'):
            # Back button
            with ui.button(on_click=lambda: ui.navigate.to('/'), color='transparent').classes(
                'p-0 border-none w-24 h-24 sm:w-28 sm:h-28 md:w-32 md:h-32'
            ):
                ui.image('/assets/Arrow.png').classes(
                    'w-full h-full object-cover rounded-xl shadow-lg'
                )

            # Text boxes next to the button (stacked on mobile)
            ui.html("""
                <div style="font-size: 18px; max-width: 300px; text-align: center;">
                    The call in the <b>green box</b> has a higher <b>frequency</b>.
                </div>
            """, sanitize=False).classes(
                "border-4 border-green-400 rounded-lg p-4 sm:p-6 shadow-md "
                "text-sm sm:text-base md:text-lg lg:text-xl"
            )
            ui.html("""
                <div style="font-size: 18px; max-width: 300px; text-align: center;">
                    The call in the <b>yellow box</b> is higher in <b>amplitude</b>.
                </div>
            """, sanitize=False).classes(
                "border-4 border-yellow-400 rounded-lg p-4 sm:p-6 shadow-md "
                "text-sm sm:text-base md:text-lg lg:text-xl"
            )
            


##########################
# --- App Info page ---
@ui.page('/app_info')
def app_info_page():
    
    # Request fullscreen on user interaction
    ui.add_head_html('''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            function tryFullscreen(e) {
                if (e.isTrusted) {
                    const elem = document.documentElement;
                    if (elem.requestFullscreen) {
                        elem.requestFullscreen().catch(err => console.log('Fullscreen:', err.message));
                    } else if (elem.webkitRequestFullscreen) {
                        elem.webkitRequestFullscreen();
                    }
                    document.removeEventListener('click', tryFullscreen);
                }
            }
            if (!document.fullscreenElement && !document.webkitFullscreenElement) {
                document.addEventListener('click', tryFullscreen, { once: true });
            }
        });
        </script>
    ''')
    
    with ui.column().classes("w-full min-h-screen items-center justify-start bg-gray-100 px-4 py-6"):

        with ui.row().classes("justify-center w-full mb-4"):
            ui.label('App Info').classes('text-2xl sm:text-3xl md:text-4xl text-center font-bold')
        
        with ui.row().props('flat bordered').style('padding:20px; border-radius: 15px'):
            ui.html("""
                    <div style="font-size: 22px; max-width: 800px; text-align: center;">
                    This app was created and designed by <b>Katie Howard</b> for the exhibition <i>'Litoria's Wetland World'</i>.<br><br>
                    Sound files were provided by the Arthur Rylah Institute for Environmental Research (DEECA) and compiled with help from Louise Durkin.<br>
                    Spectrograms were created using PASE (Python-Audio-Spectrogram-Explorer).<br><br>
                    All photos provided by Katie Howard except for those listed below, which are used with permission from:<br>
                    - Zak Atkins: Peron's Tree Frog<br>
                    - Geoff Heard : Pobblebonk Frog and Spotted Marsh Frog<br>
                    </div>
            """, sanitize=False)
        
        with ui.row().style('justify-content: center; gap: 10px; margin-top: 10px; flex-wrap: wrap;'):
            # Back button
            with ui.button(on_click=lambda: ui.navigate.to('/'), color='transparent').style(
                'padding:0; border:none; width: 180px; height: 180px;'
            ):
                ui.image('/assets/Arrow.png').style(
                    'width: 100%; height: 100%; object-fit: cover; border-radius: 15px; '
                    'box-shadow: 0 4px 10px rgba(0,0,0,0.4);'
                )


#################################
# --- Individual frog page ---
# --- Frog Detail Page ---
@ui.page('/frog/{frog_name}')
def frog_detail_page(frog_name: str):
    
    # Request fullscreen on user interaction
    ui.add_head_html('''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            function tryFullscreen(e) {
                if (e.isTrusted) {
                    const elem = document.documentElement;
                    if (elem.requestFullscreen) {
                        elem.requestFullscreen().catch(err => console.log('Fullscreen:', err.message));
                    } else if (elem.webkitRequestFullscreen) {
                        elem.webkitRequestFullscreen();
                    }
                    document.removeEventListener('click', tryFullscreen);
                }
            }
            if (!document.fullscreenElement && !document.webkitFullscreenElement) {
                document.addEventListener('click', tryFullscreen, { once: true });
            }
        });
        </script>
    ''')
    
    # Simulate loading frog info
    frogs_list = [
        {"name": "Growling Grass \nFrog", "photo": "assets/GGF.png", "Species name": "Ranoidea (nee Litoria) raniformis",
        "video": "assets/GGF_resized.mp4", "preview": "assets/GGF_spec_safe3_preview.jpg",
        "ind_name": "Growling Grass Frog"},
        {"name": "Southern Brown \nTree Frog", "photo": "assets/SBTF.png", "Species name": "Litoria ewingii", 
        "video": "assets/SBTF_resized.mp4", "preview":"assets/SBTF_spec_safe3_preview.jpg",
        "ind_name": "Southern Brown Tree Frog"},
        {"name": "Peron's Tree \nFrog", "photo": "assets/PTF.png", "Species name": "Litoria peronii",
        "video": "assets/PTF_resized.mp4", "preview": "assets/PTF_spec_safe3_preview.jpg",
        "ind_name": "Peron's Tree Frog"},
        {"name": "Pobblebonk \nFrog", "photo": "assets/PBF.png", "Species name": "Limnodynastes dumerili",
        "video": "assets/PBF_resized.mp4", "preview": "assets/PBF_spec_safe3_preview.jpg",
        "ind_name": "Pobblebonk Frog"},
        {"name": "Common \nFroglet", "photo": "assets/CF.png", "Species name": "Crinia signifera",
        "video": "assets/CF_resized.mp4", "preview": "assets/CF_spec_safe3_preview.jpg",
        "ind_name": "Common Froglet"},
        {"name": "Common Spadefoot \nToad", "photo": "assets/CSFT.png", "Species name": "Neobatrachus sudelli",
        "video": "assets/CSFT_resized.mp4", "preview": "assets/CSFT_spec_safe3_preview.jpg",
        "ind_name": "Sudell's Frog"},
        {"name": "Eastern Sign-bearing \nFroglet", "photo": "assets/ESBF.png", "Species name" : "Geocrinia victoriana",
        "video": "assets/ESBF_resized.mp4", "preview": "assets/ESBF_spec_safe3_preview.jpg",
        "ind_name": "Eastern Sign-bearing Froglet"},
        {"name": "Spotted Marsh \nFrog", "photo": "assets/SMF.png", "Species name" : "Limnodynastes tasmaniensis",
        "video": "assets/SMF_resized.mp4", "preview": "assets/SMF_spec_safe3_preview.jpg",
        "ind_name": "Spotted Marsh Frog"},
    ]
    frog = next((f for f in frogs_list if f['ind_name'] == frog_name), None)
    if not frog:
        ui.label('Frog not found!').classes('text-red-500 text-xl')
        return

    with ui.column().classes("w-full h-screen justify-center bg-white"):
        # --- Header ---
        with ui.row().classes('justify-center items-center w-full'):
            ui.label(frog["ind_name"]).classes('text-3xl font-bold')
            ui.label(frog["Species name"]).classes('text-3xl font-bold italic ml-2')


        # --- Video (no native controls) ---
        video = ui.video(resource_path(frog["video"])).props('preload="auto" muted disablepictureinpicture').classes(
            "w-full max-w-5x1 h-auto rounded-xl shadow-md border border-gray-300"
        ).style('pointer-events: none;')
        
        # Hide controls completely with CSS
        ui.add_head_html('''
            <style>
            video::-webkit-media-controls {
                display: none !important;
            }
            video::-webkit-media-controls-enclosure {
                display: none !important;
            }
            video::-webkit-media-controls-panel {
                display: none !important;
            }
            video::-moz-media-controls {
                display: none !important;
            }
            video::-ms-media-controls {
                display: none !important;
            }
            </style>
        ''')
        
        # pause initially to show first frame (no autoplay)
        ui.run_javascript('document.querySelector("video").pause()')

        play_icon = None
        ## Controls row ---
        with ui.row().classes('w-full justify-between items-start'):

            

            # ▶️ Play button (we’ll reference it later)
            with ui.button(color='transparent', on_click=lambda:toggle_video).style(
            'padding:0; border:none; width:180px; height:180px;') as play_button:
                # now assign to outer-scope variable using 'nonlocal'
                def set_icon():
                    nonlocal play_icon
                    play_icon = ui.image(resource_path('PLAY.png')).style(
                        'width:100%; height:100%; object-fit:cover; border-radius:15px; '
                        'box-shadow:0 4px 10px rgba(0,0,0,0.4);'
                    )
                set_icon()

            # 🐸 Frog image
            ui.image(resource_path(frog["photo"])).classes(
                'w-64 h-64 object-contain rounded-xl shadow-md'
            )
                
            
            # ⬅️ Back button (arrow)
            with ui.button(on_click=lambda: ui.navigate.to('/'), color='transparent').style(
                'padding:0; border:none; width: 180px; height: 180px;'
            ):
                ui.image('/assets/Arrow.png').style(
                    'object-fit: cover; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.4);'
                )

        # --- Toggle logic ---
        def toggle_video():
        # toggle play/pause in browser and unmute when playing
            ui.run_javascript("""
                const video = document.querySelector('video');
                if (video.paused) { 
                    video.muted = false;  // Unmute when playing
                    video.play(); 
                } 
                else { 
                    video.pause(); 
                }
            """)
        # update play icon
            if play_icon.source.endswith('PLAY.png'):
                play_icon.source = resource_path('PAUSE.png')
            else:
                play_icon.source = resource_path('PLAY.png')
        
        play_button.on('click', toggle_video)

#################################
## -----Mystery Frog Page----##
@ui.page('/mystery')
def mystery_frog_page():

    # Request fullscreen on user interaction
    ui.add_head_html('''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            function tryFullscreen(e) {
                if (e.isTrusted) {
                    const elem = document.documentElement;
                    if (elem.requestFullscreen) {
                        elem.requestFullscreen().catch(err => console.log('Fullscreen:', err.message));
                    } else if (elem.webkitRequestFullscreen) {
                        elem.webkitRequestFullscreen();
                    }
                    document.removeEventListener('click', tryFullscreen);
                }
            }
            if (!document.fullscreenElement && !document.webkitFullscreenElement) {
                document.addEventListener('click', tryFullscreen, { once: true });
            }
        });
        </script>
    ''')

    # Simulate loading frog info
    frogs_list = [
        {"name": "Growling Grass \nFrog", "photo": "assets/GGF.png", "Species name": "Ranoidea (nee Litoria) raniformis",
        "video": "assets/GGF_resized.mp4", "preview": "assets/GGF_spec_safe3_preview.jpg",
        "ind_name": "Growling Grass Frog"},
        {"name": "Southern Brown \nTree Frog", "photo": "assets/SBTF.png", "Species name": "Litoria ewingii", 
        "video": "assets/SBTF_resized.mp4", "preview":"assets/SBTF_spec_safe3_preview.jpg",
        "ind_name": "Southern Brown Tree Frog"},
        {"name": "Peron's Tree \nFrog", "photo": "assets/PTF.png", "Species name": "Litoria peronii",
        "video": "assets/PTF_resized.mp4", "preview": "assets/PTF_spec_safe3_preview.jpg",
        "ind_name": "Peron's Tree Frog"},
        {"name": "Pobblebonk \nFrog", "photo": "assets/PBF.png", "Species name": "Limnodynastes dumerili",
        "video": "assets/PBF_resized.mp4", "preview": "assets/PBF_spec_safe3_preview.jpg",
        "ind_name": "Pobblebonk Frog"},
        {"name": "Common \nFroglet", "photo": "assets/CF.png", "Species name": "Crinia signifera",
        "video": "assets/CF_resized.mp4", "preview": "assets/CF_spec_safe3_preview.jpg",
        "ind_name": "Common Froglet"},
        {"name": "Common Spadefoot \nToad", "photo": "assets/CSFT.png", "Species name": "Neobatrachus sudelli",
        "video": "assets/CSFT_resized.mp4", "preview": "assets/CSFT_spec_safe3_preview.jpg",
        "ind_name": "Sudell's Frog"},
        {"name": "Eastern Sign-bearing \nFroglet", "photo": "assets/ESBF.png", "Species name" : "Geocrinia victoriana",
        "video": "assets/ESBF_resized.mp4", "preview": "assets/ESBF_spec_safe3_preview.jpg",
        "ind_name": "Eastern Sign-bearing Froglet"},
        {"name": "Spotted Marsh \nFrog", "photo": "assets/SMF.png", "Species name" : "Limnodynastes tasmaniensis",
        "video": "assets/SMF_resized.mp4", "preview": "assets/SMF_spec_safe3_preview.jpg",
        "ind_name": "Spotted Marsh Frog"},
    ]

            # --- Reactive state ---
    state = {
        "current_frog": random.choice(frogs_list),
        "revealed": False,
        "playing": False,
        "show_try_again": False,
        "option_buttons": {},
    }

    # --- FUNCTIONS ---
    def build_frog_options(container, correct_frog):
        """Generate multiple-choice answer buttons"""
        container.clear()
        
        # Get other frogs as options (comparing by entire frog object)
        options = random.sample(
            [f for f in frogs_list if f["ind_name"] != correct_frog["ind_name"]],
            k=min(7, len(frogs_list) - 1)
        )
        options.append(correct_frog)
        random.shuffle(options)
        
        # Store button references for later highlighting
        state["option_buttons"] = {}
        
        with container:
            with ui.grid(columns=4).classes("gap-2 justify-center mt-2 grid-cols-1 md:grid-cols-4 w-full px-2"):
                for frog in options:
                    btn = ui.button(
                        frog["name"], 
                        on_click=lambda _, f=frog: check_answer(f, correct_frog)
                    ).classes(
                        "bg-green-700 text-white font-semibold text-sm md:text-md rounded-md px-2 py-2 "
                        "hover:bg-green-800 transition-all h-auto md:h-16 w-full"
                    )
                    # Store button reference with the frog ind_name as key
                    state["option_buttons"][frog["ind_name"]] = btn
                    
                    
    def check_answer(selected_frog, correct_frog):
        """Reveal result and highlight correct answer - matching Kivy behavior"""
        if state["revealed"]:
            return
        state["revealed"] = True
        state["show_try_again"] = True

        # Visual feedback for all buttons (matching Kivy implementation)
        for frog_id, btn in state.get("option_buttons", {}).items():
            if frog_id == selected_frog["ind_name"]:
                # Selected answer gets black border
                btn.style("border: 3px solid black")
            
            if frog_id == correct_frog["ind_name"]:
                # Correct answer gets yellow/gold background (matching Kivy's (1, 0.84, 0, 1))
                # Using direct style for more reliable color change
                btn.style("background-color: #fbbf24 !important")  # Tailwind yellow-400
            elif frog_id != selected_frog["ind_name"]:
                # Other incorrect answers fade out
                btn.style("opacity: 0.3")

        # Update result text
        if selected_frog["ind_name"] == correct_frog["ind_name"]:
            result_label.set_text(f"✅ Correct! It's the {correct_frog['name'].replace(chr(10), ' ')}")
            result_label.classes(remove="text-red-600")
            result_label.classes(add="text-green-600 font-bold text-xl")
        else:
            result_label.set_text(f"❌ Oops! It was the {correct_frog['name'].replace(chr(10), ' ')}")
            result_label.classes(remove="text-green-600")
            result_label.classes(add="text-red-600 font-bold text-xl")

       
    def try_again():
        """Pick a new random frog and reset the quiz"""
        state["current_frog"] = random.choice(frogs_list)
        state["revealed"] = False
        state["show_try_again"] = False  #hides the button again
        result_label.set_text("")

        # reset video
        video.source = state["current_frog"]["video"]
        video.run_method("pause")
        state["playing"] = False
        play_icon.set_source("assets/PLAY.png")

        # rebuild options
        build_frog_options(options_container, state["current_frog"])


    def toggle_video():
        """Play or pause the current video"""
        if state["playing"]:
            video.run_method("pause")
            play_icon.set_source("assets/PLAY.png")
        else:
            # Unmute and play when play button is clicked
            ui.run_javascript("""
                const video = document.querySelector('video');
                video.muted = false;
            """)
            video.run_method("play")
            play_icon.set_source("assets/PAUSE.png")
        state["playing"] = not state["playing"]




    # --- PAGE LAYOUT ---
    with ui.column().classes("w-full h-screen items-center justify-start bg-white"):

        # Header
        ui.label("🐸 Mystery Frog Quiz").classes(
            "text-3xl font-bold text-center text-green-800 mb-4"
        )

        # Video (paused initially, no controls, muted by default)
        video = ui.video(state["current_frog"]["video"]).props(
            'muted disablepictureinpicture'
        ).classes(
            "w-full max-w-5x1 h-auto rounded-xl shadow-md border border-gray-300"
        ).style('pointer-events: none;')
        
        # Hide all video controls with CSS
        ui.add_head_html('''
            <style>
            video::-webkit-media-controls {
                display: none !important;
            }
            video::-webkit-media-controls-enclosure {
                display: none !important;
            }
            video::-webkit-media-controls-panel {
                display: none !important;
            }
            video::-moz-media-controls {
                display: none !important;
            }
            video::-ms-media-controls {
                display: none !important;
            }
            </style>
        ''')

          # --- BOTTOM SECTION ---
        with ui.row().classes("w-full justify-between items-start"):

            # --- LEFT CONTROL STACK (Home + Play vertically stacked) ---
            with ui.column().classes("flex-none items-center justify-center"):
                # Home button
                with ui.button(on_click=lambda: ui.navigate.to("/"), color="transparent").style(
                    "padding:0; border:none; width:160px; height:160px;"
                ):
                    ui.image("/assets/Arrow.png").style(
                        "width:100%; height:100%; object-fit:cover; border-radius:5px; "
                        "box-shadow:0 4px 10px rgba(0,0,0,0.4);"
                    )
            # Play button
            with ui.column().classes("flex-none items-center justify-center gap-4"):
                with ui.button(on_click=toggle_video).classes("w-20 h-20 bg-transparent p-0 border-none").style(
                    "padding: 0; border: none; width: 160px; height: 160px;"
                ):
                    play_icon = ui.image("/assets/PLAY.png").style(
                        "width:100%; height:100%; object-fit:contain;"
                    )


            # --- RIGHT (Quiz section) ---
            with ui.column().classes(
                "flex-1 items-center justify-start p-0 bg-gray-50 rounded-lg m-0" \
                "shadow-sm border border-gray-200"):
                ui.label("Guess the Frog:").classes(
                    "text-2xl font-semibold text-center text-black"
                )

                options_container = ui.column().classes("items-center justify-center")
                build_frog_options(options_container, state["current_frog"])

                result_label = ui.label("").classes("text-xl font-semibold text-center justify-left mt-1")

                try_again_button = ui.button("🔄 Try Again?", on_click=try_again).classes(
                    "bg-yellow-500 text-black font-bold text-xl mt-2 rounded-md shadow-md hover:bg-yellow-400 transition-all"
                )
                

# --- Run the app ---
#if __name__ in {"__main__", "__mp_main__"}:
#    from main_activity import start_webview
#    ui.run(host='0.0.0.0', port=8080, reload=False)
#    start_webview()
# --- Android WebView support ---
if platform.system() == 'Android':
    from main_activity import start_webview
else:
    # Desktop stub
    def start_webview():
        pass


# --- Setup for both Uvicorn (Railway/PaaS) and direct execution ---

# Get port from environment variable (for Railway, Render, etc.) or default to 8080
PORT = int(os.environ.get('PORT', 8080))

print(f"🐸 Starting Frog Quiz app on port {PORT}")
print(f"Platform: {platform.system()}")
print(f"Assets directory: {Path(__file__).parent / 'assets'}")

# Initialize ui.run() for module-level (required when uvicorn loads this module)
# This doesn't start the server yet, just configures NiceGUI properly
ui.run(
    host='0.0.0.0',
    port=PORT,
    reload=False,
    show=False,
    title='Frog Quiz - Educational App',
    uvicorn_logging_level='info'
)

# When running directly (not via uvicorn)
if __name__ in {"__main__", "__mp_main__"}:
    if platform.system() == 'Android':
        start_webview()
