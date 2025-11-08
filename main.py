from nicegui import ui, app
from datetime import datetime
from pathlib import Path
import random
import platform
import os


## local assets folder
app.add_static_files('/assets', Path(__file__).parent / 'assets')

## def helper function 
def resource_path(rel_path: str) -> str:
    # return proper URL path for assets
    if rel_path.startswith('assets/'):
        rel_path = rel_path.replace('assets/', '', 1)
    return f'/assets/{rel_path}'


## Frog data 
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


# --- Home page ---
@ui.page('/')
def home_page():  

    # ✅ Set the background color for the whole page
    ui.query('body').classes('bg-green-700')  # Tailwind green
    ui.query('body').style('background-color: #2E8B57;')  # fallback if classes don't apply

    # ✅ Title label
    with ui.row().classes("justify-center items-center w-full"):
        ui.label('Select a frog to see and hear its call').style(
        'font-size: 36px; text-align: center; margin: 20px 0; color: white;'
    )

    # ✅ Responsive grid layout

    with ui.grid(columns=5).style(
        'gap: 25px; justify-items: center; align-items: start; '
        'width: 100%; padding: 20px; max-width: 1400px; margin: 0 auto;'
    ):
        with ui.column().style('align-items: center; gap: 5px;'):
            with ui.button(color='transparent', on_click=lambda: ui.navigate.to('/instructions')).style(
                        'padding:0; border:none; height: 250 px; width: 250px; aspect-ratio: 1 / 1;'
                    ):
                        ui.image('assets/App_overview.png').style(
                            'width: 100%; height: 100%; object-fit: cover; border-radius: 15px; '
                            'box-shadow: 0 4px 10px rgba(0,0,0,0.3);'
                        )
            ui.label("How spectrograms show sound").style(
                    'font-size: 24px; font-weight: 500; text-align: center; color: white;'
                )     
        for frog in frogs_list:
            with ui.column().style('align-items: center; gap: 5px;'):  
                    # Button only contains the image
                with ui.button(color='transparent',
                    on_click=lambda f=frog: ui.navigate.to(f'/frog/{f["ind_name"]}'),).style(
                    'padding:0; border:none; height: 250 px; width: 250px; aspect-ratio: 1 / 1;'
                    ):
                        ui.image(frog['photo']).style(
                            'width: 100%; height: 100%; object-fit: cover; border-radius: 15px; '
                            'box-shadow: 0 4px 10px rgba(0,0,0,0.3);'
                        )
                    
                # Label below the button
                ui.label(frog['name']).style(
                    'font-size: 24px; font-weight: 500; text-align: center; color: white;'
                )
            
        with ui.column().style('align-items: center; gap: 5px;'):
            with ui.button(color='transparent', on_click=lambda: ui.navigate.to('/mystery')).style(
                        'padding:0; border:none; height: 250 px; width: 250px; aspect-ratio: 1 / 1;'
                    ):
                        ui.image('assets/UnknownFrog.png').style(
                            'width: 100%; height: 100%; object-fit: cover; border-radius: 15px; '
                            'box-shadow: 0 4px 10px rgba(0,0,0,0.3);'
                        )
            ui.label("Mystery Frog").style(
                    'font-size: 24px; font-weight: 500; text-align: center; color: white;'
                )     
      
                    

    # ✅ App info button at bottom
    ui.button('App Info', on_click=lambda: ui.navigate.to('/app_info')).props('raised')\
        .style('font: Poppins; background-color: #4CAF50; color: white; font-size: 20px; padding: 10px 20px; margin-top: 20px;')

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

    # 🌿 Background (optional, to match your theme)
    #ui.query('body').style('background-color: #2E8B57; color: white;')

    with ui.column().classes("w-full h-screen items-center justify-start bg-white"):
        # --- Header ---
        with ui.row().classes("items-center justify-center w-full"):
            ui.label('Spectrograms display the frequency and amplitude of sound')\
            .style('font-size: 32px; text-align: center; text-justify: center; margin-bottom: 10px; font-weight: bold; color: darkgreen')

        # --- Top Info Boxes (Two side-by-side) ---
        with ui.row().style('justify-content: center; gap: 200px; margin-bottom: 10px; flex-wrap: wrap;'):
            ui.html("""
                <div style="font-size: 22px; max-width: 500px; max-height: 300px; text-align: left;">
                    Sounds are vibrations and the number of vibrations per second
                    determines the <b>frequency</b> or pitch of a sound.<br>
                    <b>Low pitch:</b> drum roll, growl<br>
                    <b>High pitch:</b> whistle, jingling keys
                </div>
            """, sanitize=False)
            ui.html("""
                <div style="font-size: 22px; max-width: 500px; max-height: 300px; text-align: left;">
                    The size of sound waves determines <b>amplitude</b> — the larger the wave, the louder the sound.<br>
                    <b>Low amplitude:</b> whispering<br>
                    <b>High amplitude:</b> yelling
                </div>
            """, sanitize=False)

        # --- Middle Image ---
        ui.image('assets/example.png').classes("w-full max-w-5x1 h-auto rounded-xl shadow-md border border-gray-300")

        # --- Bottom Row: Back Button + 2 Text Boxes ---
        with ui.row().style('justify-content: center; gap: 200px; margin-top: 10px; flex-wrap: wrap;'):
            # Back button
            with ui.button(on_click=lambda: ui.navigate.to('/'), color='transparent').style(
                'padding:0; border:none; width: 120px; height: 120px;'
            ):
                ui.image('assets/Arrow.png').style(
                    'width: 100%; height: 100%; object-fit: cover; border-radius: 15px; '
                    'box-shadow: 0 4px 10px rgba(0,0,0,0.4);'
                )

            # Text boxes next to the button
            ui.html("""
                <div style="font-size: 22px; max-width: 300px; text-align: center;">
                    The call in the <b>green box</b> has a higher <b>frequency</b>.
                </div>
            """, sanitize=False).classes("border-4 border-green-400 rounded-x6 p-6 shadow-md")
            ui.html("""
                <div style="font-size: 22px; max-width: 300px; text-align: center;">
                    The call in the <b>yellow box</b> is higher in <b>amplitude</b>.
                </div>
            """, sanitize=False).classes("border-4 border-yellow-400 rounded-x6 p-6 shadow-md")
            


##########################
# --- App Info page ---
@ui.page('/app_info')
def app_info_page():
    
    with ui.column().classes("w-full h-screen items-center justify-start bg-lightgrey"):

        with ui.row().classes("justify-centre w-full"):
            ui.label('App Info').style('font-size:36px; text-align:center; margin-bottom:0px;')
        
        with ui.row().props('flat bordered').style('padding:20px; border-radius: 15px'):
            ui.html("""
                    <div style="font-size: 22px; max-width: 300px; text-align: center;">
                    This app was created and designed by <b>Katie Howard</b> for the exhibition <i>‘Litoria’s Wetland World’</i>.<br><br>
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
                ui.image('assets/Arrow.png').style(
                    'width: 100%; height: 100%; object-fit: cover; border-radius: 15px; '
                    'box-shadow: 0 4px 10px rgba(0,0,0,0.4);'
                )


#################################
# --- Individual frog page ---
# --- Frog Detail Page ---
@ui.page('/frog/{frog_name}')
def frog_detail_page(frog_name: str):
    
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
        video = ui.video(resource_path(frog["video"])).props('preload="auto" autoplay muted controlslist="nodownload nofullscreen noremoteplayback" disablepictureinpicture controls=false').classes(
            "w-full max-w-5x1 h-auto rounded-xl shadow-md border border-gray-300"
        )
        # pause initially to show first frame
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
                ui.image('assets/Arrow.png').style(
                    'object-fit: cover; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.4);'
                )

        # --- Toggle logic ---
        def toggle_video():
        # toggle play/pause in browser
            ui.run_javascript("""
                const video = document.querySelector('video');
                if (video.paused) { video.play(); } 
                else { video.pause(); }
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
    }

    # --- FUNCTIONS ---
    def build_frog_options(container, correct_frog):
        """Generate multiple-choice answer buttons"""
        container.clear()
        correct_name = correct_frog["name"]
        options = random.sample(
            [f["name"] for f in frogs_list if f != correct_frog],
            k=min(7, len(frogs_list) - 1)
        )
        options.append(correct_name)
        random.shuffle(options)
        
        with container:
            with ui.grid(columns=4).classes("gap-1 justify-center mt-1"):
                for name in options:
                    
                    ui.button(name, on_click=lambda _, n=name: check_answer(n, correct_name),
                    ).classes(
                        "bg-green-700 text-white font-semibold text-md rounded-md px-2 py-1 m-1"
                        "hover:bg-green-800 transition-all h-16 w-63")
                    
                    
    def check_answer(selected, correct):
        """Reveal result and highlight correct answer"""
        if state["revealed"]:
            return
        state["revealed"] = True
        state["show_try_again"] = True

        if selected == correct:
            result_label.set_text(f"✅ Correct! It’s the {correct}.").classes("text-green-600 font-bold text-xl")
        else:
            result_label.set_text(f"❌ Oops! It was the {correct}.").classes("text-red-600 font-bold text-xl")

       
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
            video.run_method("play")
            play_icon.set_source("assets/PAUSE.png")
        state["playing"] = not state["playing"]




    # --- PAGE LAYOUT ---
    with ui.column().classes("w-full h-screen items-center justify-start bg-white"):

        # Header
        ui.label("🐸 Mystery Frog Quiz").classes(
            "text-3xl font-bold text-center text-green-800 mb-4"
        )

        # Video (paused initially, no controls)
        video = ui.video(state["current_frog"]["video"]).props(
            'controls=false controlslist="nodownload nofullscreen noremoteplayback"'
        ).classes(
            "w-full max-w-5x1 h-auto rounded-xl shadow-md border border-gray-300"
        )

          # --- BOTTOM SECTION ---
        with ui.row().classes("w-full justify-between items-start"):

            # --- LEFT CONTROL STACK (Home + Play vertically stacked) ---
            with ui.column().classes("flex-none items-center justify-center"):
                # Home button
                with ui.button(on_click=lambda: ui.navigate.to("/"), color="transparent").style(
                    "padding:0; border:none; width:160px; height:160px;"
                ):
                    ui.image("assets/Arrow.png").style(
                        "width:100%; height:100%; object-fit:cover; border-radius:5px; "
                        "box-shadow:0 4px 10px rgba(0,0,0,0.4);"
                    )
            # Play button
            with ui.column().classes("flex-none items-center justify-center gap-4"):
                with ui.button(on_click=toggle_video).classes("w-20 h-20 bg-transparent p-0 border-none").style(
                    "padding: 0; border: none; width: 160px; height: 160px;"
                ):
                    play_icon = ui.image("assets/PLAY.png").style(
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


#When testing desktop


if __name__ in {"__main__", "__mp_main__"}:
    # Get port from environment variable (for Railway, Render, etc.) or default to 8080
    port = int(os.environ.get('PORT', 8080))
    
    print(f"🐸 Starting Frog Quiz app on port {port}")
    print(f"Platform: {platform.system()}")
    print(f"Assets directory: {Path(__file__).parent / 'assets'}")
    
    if platform.system() == 'Android':
        ui.run(host='0.0.0.0', port=8080, reload=False)
        start_webview()
    else:
        ui.run(
            host='0.0.0.0', 
            port=port, 
            reload=False, 
            show=False,
            title='Frog Quiz - Educational App'
        )
