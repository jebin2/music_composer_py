from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
import gc
import importlib.resources

with importlib.resources.path("music_composer", "templates") as tpl_path:
    template_folder=str(tpl_path)
with importlib.resources.path("music_composer", "static") as static_path:
    static_folder=str(static_path)

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)


instrumentMap = {
    "piano": [
        "acoustic_grand",
        "bright_acoustic",
        "electric_grand",
        "honky_tonk",
        "electric_piano_1",
        "electric_piano_2",
        "electric_piano",
        "piano"
    ],
    "keyboard": [
        "harpsichord",
        "clavinet",
        "clavichord",
        "celesta",
        "music_box"
    ],
    "bells": [
        "glockenspiel",
        "church_bells",
        "tubular_bells",
        "tinkle_bell"
    ],
    "mallet": [
        "vibraphone",
        "marimba",
        "xylophone",
        "dulcimer",
        "kalimba"
    ],
    'organ': [
        "drawbar_organ",
        "percussive_organ",
        "rock_organ",
        "church_organ",
        "pipe_organ",
        "reed_organ",
        "electric_organ",
        "organ"
    ],
    "guitar": [
        "acoustic_guitar_nylon",
        "acoustic_guitar_steel",
        "electric_guitar_jazz",
        "electric_guitar_clean",
        "electric_guitar_muted",
        "overdriven_guitar",
        "distortion_guitar",
        "guitar_harmonics",
        "acoustic_guitar",
        "electric_guitar",
        "guitar",
        "lute",
        "mandolin",
        "ukulele"
    ],
    "bass": [
        "acoustic_bass",
        "electric_bass_finger",
        "electric_bass_pick",
        "fretless_bass",
        "slap_bass_1",
        "slap_bass_2",
        "synth_bass_1",
        "synth_bass_2",
        "electric_bass"
    ],
    "strings": [
        "violin",
        "viola",
        "cello",
        "violoncello",
        "contrabass",
        "tremolo_strings",
        "pizzicato_strings",
        "string_ensemble_1",
        "string_ensemble_2",
        "synth_strings_1",
        "synth_strings_2",
        "string_instrument",
        "fiddle"
    ],
    "harp": [
        "orchestral_harp",
        "harp"
    ],
    "percussion": [
        "timpani",
        "taiko_drum",
        "melodic_tom",
        "synth_drum",
        "woodblock",
        "agogo",
        "steel_drums",
        "steel_drum"
    ],
    "voice": [
        "choir_aahs",
        "voice_oohs",
        "synth_choir",
        "vocalist",
        "choir",
        "soprano",
        "mezzo_soprano",
        "alto",
        "tenor",
        "baritone",
        "bass"
    ],
    "brass": [
        "trumpet",
        "trombone",
        "tuba",
        "muted_trumpet",
        "french_horn",
        "brass_section",
        "synth_brass_1",
        "synth_brass_2",
        "horn",
        "brass_instrument",
        "bass_trombone"
    ],
    "reed": [
        "soprano_sax",
        "alto_sax",
        "tenor_sax",
        "baritone_sax",
        "saxophone",
        "soprano_saxophone",
        "alto_saxophone",
        "tenor_saxophone",
        "baritone_saxophone",
        "oboe",
        "english_horn",
        "bassoon",
        "contrabassoon",
        "clarinet",
        "bass_clarinet"
    ],
    "flute": [
        "piccolo",
        "flute",
        "recorder",
        "pan_flute",
        "blown_bottle",
        "shakuhachi",
        "whistle",
        "ocarina"
    ],
    "lead": [
        "lead_1_square",
        "lead_2_sawtooth",
        "lead_3_calliope",
        "lead_4_chiff",
        "lead_5_charang",
        "lead_6_voice",
        "lead_7_fifths",
        "lead_8_bass_lead"
    ],
    "pad": [
        "pad_1_new_age",
        "pad_2_warm",
        "pad_3_polysynth",
        "pad_4_choir",
        "pad_5_bowed",
        "pad_6_metallic",
        "pad_7_halo",
        "pad_8_sweep"
    ],
    "fx": [
        "fx_1_rain",
        "fx_2_soundtrack",
        "fx_3_crystal",
        "fx_4_atmosphere",
        "fx_5_brightness",
        "fx_6_goblins",
        "fx_7_echoes",
        "fx_8_sci_fi",
        "reverse_cymbal",
        "sampler",
        "orchestra_hit"
    ],
    "ethnic": [
        "sitar",
        "banjo",
        "shamisen",
        "koto",
        "bagpipe",
        "bagpipes",
        "shanai",
        "shehnai",
        "taiko"
    ],
    "sfx": [
        "guitar_fret_noise",
        "breath_noise",
        "seashore",
        "bird_tweet",
        "telephone_ring",
        "helicopter",
        "applause",
        "gunshot"
    ]
}

# Web page (form to create music)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    output_file = None
    composer_instance = None
    try:
        data = request.get_json()
        text = data.get("text", "")
        instruments = data.get("instruments", []) # Default to empty list
        all_inst = None
        if instruments:
            all_inst = [inst for k in instruments if k in instrumentMap for inst in instrumentMap[k]]

        print(f"Generating music with instruments: {all_inst}") # Log the actual list being passed

        # Import and instantiate locally
        from music_composer import MusicComposer
        composer_instance = MusicComposer()
        output_file = composer_instance.generate_music(user_prompt=text, instruments=all_inst)

        return jsonify({
            "message": "Music generated!",
            "file": output_file
        })
    except Exception as e:
         print(f"Error during music generation: {e}")
         # import traceback; print(traceback.format_exc()) # Uncomment for detailed debug
         return jsonify({"error": "Failed to generate music"}), 500
    finally:
        # Clean up the reference explicitly (good practice, though GC should get it)
        del composer_instance
        # Suggest garbage collection
        gc.collect()
        print("gc.collect() called after generation request.")

@app.route("/api/settings", methods=["GET"])
def get_settings():
    # Load the .env file if it exists
    if os.path.exists(".env"):
        load_dotenv(dotenv_path=".env", override=True)

    # Get the value from environment variables
    gemini_key = os.getenv("GEMINI_API_KEYS", "")
    output_path = os.getenv("OUTPUT_WAV", "")

    return jsonify({
        "api_key": gemini_key,
        "instruments":[k for k, _ in instrumentMap.items()],
        "output_path":output_path
    })

@app.route("/api/settings", methods=["POST"])
def save_settings():
    data = request.get_json()
    new_key = data.get("api_key", "")

    env_path = ".env"
    lines = []
    updated = False

    # If file exists, read and try to update
    if os.path.exists(env_path):
        with open(env_path, "r") as file:
            for line in file:
                if line.startswith("GEMINI_API_KEYS="):
                    lines.append(f"GEMINI_API_KEYS=\"{new_key}\"\n")
                    updated = True
                else:
                    lines.append(line)
    else:
        # If file doesn't exist, create a new list
        lines = []

    # If not updated, add new line
    if not updated:
        lines.append(f"GEMINI_API_KEYS=\"{new_key}\"\n")

    # Write to .env (create or overwrite)
    with open(env_path, "w") as file:
        file.writelines(lines)

    # Reload environment
    load_dotenv()

    return jsonify({"message": "API Key saved successfully!"})

@app.route('/static/<path:filename>')
def serve_tmp_static(filename):
    with importlib.resources.path("music_composer", "static") as static_path:
        static_folder=str(static_path)

    if os.getenv("MUSIC_COMPOSER_BASE_PATH", None):
        static_folder = f'{os.getenv("MUSIC_COMPOSER_BASE_PATH", None)}'

    return send_from_directory(static_folder, filename)

def run_server():
    app.run(debug=False, host='0.0.0.0', port=os.getenv("SERVER_PORT", 8000))

if __name__ == "__main__":
    run_server()
