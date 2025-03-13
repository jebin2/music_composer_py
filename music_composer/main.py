from custom_logger import logger_config
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from music21 import chord, note
import subprocess
import os
from google import genai
from gemiwrap import GeminiWrapper
import json

class MusicComposer:
	__PIANO_SOUNDS = {
		# Acoustic Pianos (1-8)
		"acoustic_grand": 0,
		"bright_piano": 1,
		"electric_grand": 2,
		"honky_tonk": 3,
		"electric_piano1": 4,  # Rhodes Piano
		"electric_piano2": 5,  # Chorused Piano
		"harpsichord": 6,
		"clavinet": 7,
		
		# Chromatic Percussion (9-16)
		"celesta": 8,
		"glockenspiel": 9,
		"music_box": 10,
		"vibraphone": 11,
		"marimba": 12,
		"xylophone": 13,
		"tubular_bells": 14,
		"dulcimer": 15,
		
		# Organs (17-24)
		"drawbar_organ": 16,
		"percussive_organ": 17,
		"rock_organ": 18,
		"church_organ": 19,
		"reed_organ": 20,
		"accordion": 21,
		"harmonica": 22,
		"tango_accordion": 23,
		
		# Other keyboard instruments
		"synth_piano": 80,
		"synth_bell": 98,
		"synth_pad": 89
	}

	def __init__(self, model_name="gemini-2.0-flash", system_instruction=None, piano_type="acoustic_grand", duration=480):
		self.__model_name = model_name
		self.__system_instruction = system_instruction
		if not self.__system_instruction:
			file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_prompt.txt")
			with open(file_path, 'r', encoding='utf-8') as file:
				self.__system_instruction = file.read()

		self.__geminiWrapper = GeminiWrapper(
			model_name=self.__model_name,
			system_instruction=self.__system_instruction,
			delete_files=True
		)
		# self.__soundfont_path = f'{os.path.dirname(os.path.abspath(__file__))}/GeneralUser-GS.sf2'
		self.__soundfont_path = f'{os.path.dirname(os.path.abspath(__file__))}/FluidR3_GM.sf2'
		self.__output_midi = f'{os.path.dirname(os.path.abspath(__file__))}/output.mid'
		self.__output_wav = os.getenv("OUTPUT_WAV")
		self.__piano_type = piano_type
		self.__duration = duration

	def __get_midi_notes(self, music_str):
		try:
			if isinstance(music_str, str):  # Single note (e.g., "C4")
				return [note.Note(music_str).pitch.midi]
			else:  # Chord (e.g., ["C4", "E4", "G4"] or chord names like "Cmaj", "Dmin7", "F#dim")
				# if all(isinstance(n, str) for n in music_str):
				#     return [note.Note(n).pitch.midi for n in music_str]
				# else:
				return [p.midi for p in chord.Chord(music_str).pitches]
		except Exception as e:
			logger_config.warning(f"Skipping {music_str}. {e}.")
			return []

	def __create_midi_file(self, music_info):
		try:
			mid = MidiFile()
			track = MidiTrack()
			mid.tracks.append(track)

			tempo = music_info.get("tempo", 90)
			track.append(MetaMessage('set_tempo', tempo=bpm2tempo(tempo)))

			time_sig = music_info.get("time_signature", "4/4")
			numerator, denominator = map(int, time_sig.split('/')) if '/' in time_sig else (4, 4)
			track.append(MetaMessage('time_signature', numerator=numerator, denominator=denominator, clocks_per_click=24, notated_32nd_notes_per_beat=8))

			track.append(MetaMessage('key_signature', key=music_info["key_signature"]))

			program_number = self.__PIANO_SOUNDS.get(self.__piano_type, 0)
			track.append(Message('program_change', program=program_number, time=0))

			for music_str in music_info["notes"]:
				note_duration = float(music_str["duration"]) if "duration" in music_str else 1.0
				velocity = int(music_str["velocity"]) if "velocity" in music_str else 64
				ticks = int(self.__duration * note_duration)

				if music_str["type"] == "note":
					midi_notes = self.__get_midi_notes(music_str["pitch"])
				elif music_str["type"] == "chord":
					midi_notes = self.__get_midi_notes(music_str["pitches"])
				else:
					continue

				if not midi_notes:
					continue

				for i, note_value in enumerate(midi_notes):
					track.append(Message('note_on', note=note_value, velocity=velocity, time=0 if i > 0 else 0))

				for i, note_value in enumerate(midi_notes):
					if i < len(midi_notes) - 1:
						track.append(Message('note_off', note=note_value, velocity=0, time=0))
					else:
						track.append(Message('note_off', note=note_value, velocity=0, time=ticks))

			if os.path.exists(self.__output_midi):
				os.remove(self.__output_midi)

			mid.save(self.__output_midi)
			logger_config.info(f"MIDI file created: {self.__output_midi}.")
		except Exception as e:
			logger_config.error(f"Error creating MIDI file: {e}", play_sound=False)

	def __convert_midi_to_wav(self):
		try:
			if os.path.exists(self.__output_wav):
				os.remove(self.__output_wav)

			command = f"fluidsynth -ni {self.__soundfont_path} {self.__output_midi} -F {self.__output_wav} -r 44100"
			subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL)
			logger_config.info(f"WAV file created: {self.__output_wav}")
		except subprocess.CalledProcessError as e:
			logger_config.error(f"Error: Failed to convert MIDI to WAV: {e}", play_sound=False)

	def __schema(self):
		return genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["key_signature", "tempo", "time_signature", "notes"],
            properties = {
                "key_signature": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "tempo": genai.types.Schema(
                    type = genai.types.Type.NUMBER,
                ),
                "time_signature": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "notes": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["type", "duration", "velocity"],
                        properties = {
                            "type": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "pitch": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "pitches": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "duration": genai.types.Schema(
                                type = genai.types.Type.NUMBER,
                            ),
                            "velocity": genai.types.Schema(
                                type = genai.types.Type.NUMBER,
                            ),
                        },
                    ),
                ),
            },
        )

	def generate_music(self, user_prompt):
		music_meta = self.__geminiWrapper.send_message(user_prompt=user_prompt, schema=self.__schema())[0]
		self.__create_midi_file(json.loads(music_meta))
		self.__convert_midi_to_wav()