# Music Composer

Create music with AI by simply describing what you want. This project uses Google's Gemini AI to generate musical compositions based on text descriptions.

## Overview

Music Composer is a Python application that translates natural language descriptions into musical compositions. By leveraging Google's Gemini API, it analyzes the emotional content, narrative structure, and context of your text to generate appropriate musical pieces.

## Features

- Generate music from text descriptions
- Convert AI-generated compositions into MIDI files
- Option to render MIDI files as WAV audio
- Customize instrument sounds and musical parameters
- Standalone application with Docker support

## Requirements

### System Dependencies
- Python 3.7+
- Git
- FluidSynth and libfluidsynth-dev (for audio rendering)

### Python Dependencies
- music21
- mido
- python-dotenv
- custom_logger
- gemiwrap

## Installation

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/jebin2/music_composer.git
cd music_composer
```

2. Install system dependencies:
```bash
# Ubuntu/Debian
apt-get update && apt-get install -y git fluidsynth libfluidsynth-dev

# macOS
brew install git fluidsynth
```

3. Install Python dependencies:
```bash
pip install -e .
```

### Option 2: Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/jebin2/music_composer.git
cd music_composer
```

2. Build and run the Docker container:
```bash
docker build -t music_composer .
docker run music_composer
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
GOOGLE_API_KEY=your_google_gemini_api_key
OUTPUT_WAV=path/to/output/file.wav
```

Required environment variables:
- `GOOGLE_API_KEY`: Your Google API key for accessing Gemini models
- `OUTPUT_WAV`: Path where the generated WAV file will be saved

## Usage

Basic usage:

```python
from music_composer import MusicComposer

# Initialize the composer
music_composer = MusicComposer()

# Generate music from a description
output_path = music_composer.generate_music("Create a 1 minute jazz piece that feels like a sunset over the ocean.")

print(f"Music generated and saved to: {output_path}")
```

### Advanced Usage

You can customize various parameters:

```python
from music_composer import MusicComposer

# Initialize with custom parameters
music_composer = MusicComposer(
    model_name="gemini-2.0-flash",
    piano_type="electric_piano1",
    duration=480,
    soundfont_path="/path/to/custom/soundfont.sf2"
)

# Generate music
output_path = music_composer.generate_music("Create a mysterious and tense composition for a horror movie scene.")
```

## Testing

To test the application in an isolated environment:

```bash
chmod +x test_in_isolated_env.sh
./test_in_isolated_env.sh
```

## APP LINK(Beta)

[Linux](https://github.com/jebin2/musiccomposer/releases/download/app-v0.1.0/musiccomposer_0.1.0_amd64.deb)

## Credits

- Created by Jebin Einstein
- Uses Google's Gemini API for music generation
- Built with music21 and FluidSynth for MIDI and audio processing