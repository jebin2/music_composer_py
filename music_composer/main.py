from custom_logger import logger_config
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from music21 import chord, note
import subprocess
import os
from google import genai
from gemiwrap import GeminiWrapper
import json
import traceback
from .drum_kit import DrumKit
from .instrument_kit import InstrumentKit
from .controller_effect_kit import ControllerEffectKit
from .pitch_bend_kit import PitchEffectKit
import random

class MusicComposer:

	def __init__(self, model_name="gemini-2.0-flash", system_instruction=None, piano_type="acoustic_grand", duration=480, soundfont_path=None, instruments=None):
		self.__model_name = model_name
		self.__system_instruction = system_instruction
		if not self.__system_instruction:
			file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_prompt.txt")
			with open(file_path, 'r', encoding='utf-8') as file:
				self.__system_instruction = file.read()

		self.__geminiWrapper = GeminiWrapper(
			model_name=self.__model_name,
			system_instruction=self.__system_instruction
		)
		if soundfont_path:
			self.__soundfont_path = soundfont_path
		else:
			self.__soundfont_path = f'{os.path.dirname(os.path.abspath(__file__))}/GeneralUser-GS.sf2'
			# self.__soundfont_path = f'{os.path.dirname(os.path.abspath(__file__))}/FluidR3_GM.sf2'
		self.__output_midi = f'{os.path.dirname(os.path.abspath(__file__))}/output.mid'
		self.__output_wav = os.getenv("OUTPUT_WAV")
		self.__piano_type = piano_type
		self.__duration = duration
		self.__instruments = instruments or [{"type": "acoustic_grand", "channel": 0}]

	def __get_midi_notes(self, music_str):
		try:
			try:
				return [int(music_str)]
			except:
				pass
			if isinstance(music_str, str):  # Single note (e.g., "C4")
				return [note.Note(music_str).pitch.midi]
			else:  # Chord (e.g., ["C4", "E4", "G4"] or chord names like "Cmaj", "Dmin7", "F#dim")
				return [p.midi for p in chord.Chord(music_str).pitches]
		except Exception as e:
			logger_config.warning(f"Skipping {music_str}. {e}.")
			return []

	def __create_midi_file(self, music_info):
		try:
			mid = MidiFile()
			
			# Create a conductor track for tempo and key signature
			conductor = MidiTrack()
			mid.tracks.append(conductor)
			
			# Set tempo
			tempo = music_info.get("tempo", 90)
			conductor.append(MetaMessage('set_tempo', tempo=bpm2tempo(tempo)))
			
			# Set time signature
			time_sig = music_info.get("time_signature", "4/4")
			numerator, denominator = map(int, time_sig.split('/')) if '/' in time_sig else (4, 4)
			conductor.append(MetaMessage('time_signature', numerator=numerator, denominator=denominator, clocks_per_click=24, notated_32nd_notes_per_beat=8))
			
			# Set key signature
			conductor.append(MetaMessage('key_signature', key=music_info["key_signature"]))
			
			# Map to store tracks by instrument
			instrument_tracks = {}
			
			# Process notes for each instrument/track
			for note_data in music_info["notes"]:
				# Get instrument info
				instrument_name = note_data.get("instrument", "acoustic_grand").lower()
				# 🎯 Detect if it's a drum/percussion instrument
				is_drum = DrumKit.is_drum(instrument_name)
				channel = 9 if is_drum else note_data.get("channel", 0)  # Drum = channel 9
				if not is_drum and channel == 9:
					channel = random.choice([i for i in range(16) if i != 9])
				
				# Create track key
				track_key = f"{instrument_name}_{channel}"
				
				# Create new track if needed
				if track_key not in instrument_tracks:
					track = MidiTrack()
					mid.tracks.append(track)
					instrument_tracks[track_key] = track
					
					if not is_drum:
						# Set instrument program
						program_number = InstrumentKit.get_program_number(instrument_name)
						track.append(Message('program_change', program=program_number, channel=channel, time=0))
				
				# Get the track
				track = instrument_tracks[track_key]

				ControllerEffectKit.add_effects(track=track, channel=channel, note_data=note_data)
				# added_pitch_bend = self.__add_pitch_bends(track=track, channel=channel, note_data=note_data)
				PitchEffectKit.add_pitch(track=track, channel=channel, ticks=self.__duration, note_data=note_data)
				
				# Process note
				note_duration = float(note_data.get("duration", 1.0))
				velocity = int(note_data.get("velocity", 64))
				ticks = int(self.__duration * note_duration)

				if is_drum:
					# 🥁 Get mapped MIDI drum note
					drum_note = DrumKit.get_midi_note(instrument_name)
					if drum_note is None:
						logger_config.warning(f"Unknown drum instrument: {instrument_name}")
						continue
					midi_notes = [drum_note]
				else:
					if note_data["type"] == "note":
						midi_notes = self.__get_midi_notes(note_data["pitch"])
					elif note_data["type"] == "chord":
						midi_notes = self.__get_midi_notes(note_data["pitches"])
					else:
						continue
				
				if not midi_notes:
					continue
				
				# Add note_on events
				for i, note_value in enumerate(midi_notes):
					track.append(Message('note_on', note=note_value, velocity=velocity, channel=channel, time=0 if i > 0 else 0))
				
				# Add note_off events
				for i, note_value in enumerate(midi_notes):
					if i < len(midi_notes) - 1:
						track.append(Message('note_off', note=note_value, velocity=0, channel=channel, time=0))
					else:
						track.append(Message('note_off', note=note_value, velocity=0, channel=channel, time=ticks))

				# if added_pitch_bend:
				# 	track.append(Message('pitchwheel', pitch=0, channel=channel, time=0))
			
			# Save the MIDI file
			if os.path.exists(self.__output_midi):
				os.remove(self.__output_midi)
			
			mid.save(self.__output_midi)
			logger_config.info(f"MIDI file created: {self.__output_midi}.")
		except Exception as e:
			logger_config.error(f"Error creating MIDI file: {e} {traceback.format_exc()}", play_sound=False)

	def __convert_midi_to_wav(self):
		try:
			if os.path.exists(self.__output_wav):
				os.remove(self.__output_wav)

			command = f"fluidsynth -ni {self.__soundfont_path} {self.__output_midi} -F {self.__output_wav} -r 44100"
			subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL)
			logger_config.info(f"WAV file created: {self.__output_wav}")
			return self.__output_wav
		except Exception as e:
			logger_config.error(f"Error: Failed to convert MIDI to WAV: {e}", play_sound=False)
			return None

	def __schema(self):
		return genai.types.Schema(
			type = genai.types.Type.OBJECT,
			required = ["key_signature", "tempo", "time_signature", "genre", "mood", "notes"],
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
				"genre": genai.types.Schema(
					type = genai.types.Type.STRING,
				),
				"mood": genai.types.Schema(
					type = genai.types.Type.STRING,
				),
				"notes": genai.types.Schema(
					type = genai.types.Type.ARRAY,
					items = genai.types.Schema(
						type = genai.types.Type.OBJECT,
						required = ["type", "duration", "velocity", "instrument", "channel", "effects"],
						properties = {
							"type": genai.types.Schema(
								type = genai.types.Type.STRING,
							),
							"pitch_bend": genai.types.Schema(
								type = genai.types.Type.NUMBER,
							),
							"pitch_bend": genai.types.Schema(
								type = genai.types.Type.OBJECT,
								required = ["start", "end", "steps"],
								properties = {
									"start": genai.types.Schema(
										type = genai.types.Type.NUMBER,
									),
									"end": genai.types.Schema(
										type = genai.types.Type.NUMBER,
									),
									"steps": genai.types.Schema(
										type = genai.types.Type.INTEGER,
									),
								},
							),
							"vibrato": genai.types.Schema(
								type = genai.types.Type.OBJECT,
								required = ["depth", "speed"],
								properties = {
									"depth": genai.types.Schema(
										type = genai.types.Type.NUMBER,
									),
									"speed": genai.types.Schema(
										type = genai.types.Type.INTEGER,
									),
								},
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
							"instrument": genai.types.Schema(
								type = genai.types.Type.STRING,
							),
							"channel": genai.types.Schema(
								type = genai.types.Type.NUMBER,
							),
							"effects": genai.types.Schema(
								type = genai.types.Type.ARRAY,
								items = genai.types.Schema(
									type = genai.types.Type.OBJECT,
									required = ["type", "value"],
									properties = {
										"type": genai.types.Schema(
											type = genai.types.Type.STRING,
										),
										"value": genai.types.Schema(
											type = genai.types.Type.NUMBER,
										),
									},
								),
							),
						},
					),
				),
			},
		)

	def generate_music(self, user_prompt: str, genre: str = None, music_data = None) -> str:
		"""
		Generate music based on user prompt and optionally specified genre
		
		Args:
			user_prompt: Text description of the desired music
			genre: Optional genre to guide the generation
		
		Returns:
			Path to generated WAV file
		"""
		# Add genre context if provided
		enhanced_prompt = f"{user_prompt} in {genre} style" if genre else user_prompt
		
		try:
			enhanced_prompt = user_prompt
		
			if not music_data:
				# Generate music data using AI model
				music_meta = self.__geminiWrapper.send_message(
					user_prompt=enhanced_prompt, 
					schema=self.__schema()
				)[0]
			
				# Convert to JSON and create MIDI file
				music_data = json.loads(music_meta)

			self.__create_midi_file(music_data)
			
			# Convert to WAV
			return self.__convert_midi_to_wav()
		except Exception as e:
			logger_config.error(f"Failed to generate music: {str(e)}")
			raise ValueError(f"Failed to generate music: {str(e)}") from e