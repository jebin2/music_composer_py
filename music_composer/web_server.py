from flask import Flask, render_template, request, jsonify
from music_composer import MusicComposer  # Assuming main has generate_music(genre)
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder='static', template_folder='templates')

# Web page (form to create music)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Form submission endpoint
@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("text", "")
    instruments = data.get("instruments", None)

    output_file = MusicComposer().generate_music(user_prompt=text, instruments=instruments)

    return jsonify({
        "message": "Music generated!",
        "file": output_file
    })

@app.route("/api/settings", methods=["GET"])
def get_settings():
    # Load the .env file if it exists
    if os.path.exists(".env"):
        load_dotenv(dotenv_path=".env", override=True)

    # Get the value from environment variables
    gemini_key = os.getenv("GEMINI_API_KEYS", "")

    return jsonify({
        "api_key": gemini_key
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

if __name__ == "__main__":
    app.run(debug=True, port=8000)
