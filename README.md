# Music Composer

Create music with AI by simply describing what you want. This project uses Google's Gemini AI to generate musical compositions based on text descriptions.

## Overview

Music Composer is a Python application that translates natural language descriptions into musical compositions. By leveraging Google's Gemini API, it analyzes the emotional content, narrative structure, and context of your text to generate appropriate musical pieces.

## Features

- Generate music from text descriptions
- Convert AI-generated compositions into MIDI files
- Option to render MIDI files as WAV audio
- Customize instrument sounds

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
chmod +x install.sh
./install.sh
```

3. Activate ENV:
```bash
source venv/bin/activate
```

4. Run Web Server:
```bash
python -m music_composer.web_server
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

Required environment variables:
- `GOOGLE_API_KEY`: Your Google API key for accessing Gemini models

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

## Testing

To test the application in an isolated environment:

```bash
chmod +x test_in_isolated_env.sh
./test_in_isolated_env.sh
```

## Credits

- Created by Jebin Einstein
- Uses Google's Gemini API for music generation
- Built with music21 and FluidSynth for MIDI and audio processing