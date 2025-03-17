from custom_logger import logger_config
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from music21 import chord, note
import subprocess
import os
from google import genai
from gemiwrap import GeminiWrapper
import json
import traceback

class MusicComposer:
	__INSTRUMENT_MAP = {
		# Piano (1-8)
		"acoustic_grand": 0,
		"bright_acoustic": 1,
		"electric_grand": 2,
		"honky_tonk": 3,
		"electric_piano_1": 4,
		"electric_piano_2": 5,
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
		
		# Organ (17-24)
		"drawbar_organ": 16,
		"percussive_organ": 17,
		"rock_organ": 18,
		"church_organ": 19,
		"reed_organ": 20,
		"accordion": 21,
		"harmonica": 22,
		"tango_accordion": 23,
		
		# Guitar (25-32)
		"acoustic_guitar_nylon": 24,
		"acoustic_guitar_steel": 25,
		"electric_guitar_jazz": 26,
		"electric_guitar_clean": 27,
		"electric_guitar_muted": 28,
		"overdriven_guitar": 29,
		"distortion_guitar": 30,
		"guitar_harmonics": 31,
		
		# Bass (33-40)
		"acoustic_bass": 32,
		"electric_bass_finger": 33,
		"electric_bass_pick": 34,
		"fretless_bass": 35,
		"slap_bass_1": 36,
		"slap_bass_2": 37,
		"synth_bass_1": 38,
		"synth_bass_2": 39,
		
		# Strings (41-48)
		"violin": 40,
		"viola": 41,
		"cello": 42,
		"contrabass": 43,
		"tremolo_strings": 44,
		"pizzicato_strings": 45,
		"orchestral_harp": 46,
		"timpani": 47,
		
		# Ensemble (49-56)
		"string_ensemble_1": 48,
		"string_ensemble_2": 49,
		"synth_strings_1": 50,
		"synth_strings_2": 51,
		"choir_aahs": 52,
		"voice_oohs": 53,
		"synth_choir": 54,
		"orchestra_hit": 55,
		
		# Brass (57-64)
		"trumpet": 56,
		"trombone": 57,
		"tuba": 58,
		"muted_trumpet": 59,
		"french_horn": 60,
		"brass_section": 61,
		"synth_brass_1": 62,
		"synth_brass_2": 63,
		
		# Reed (65-72)
		"soprano_sax": 64,
		"alto_sax": 65,
		"tenor_sax": 66,
		"baritone_sax": 67,
		"oboe": 68,
		"english_horn": 69,
		"bassoon": 70,
		"clarinet": 71,
		
		# Pipe (73-80)
		"piccolo": 72,
		"flute": 73,
		"recorder": 74,
		"pan_flute": 75,
		"blown_bottle": 76,
		"shakuhachi": 77,
		"whistle": 78,
		"ocarina": 79,
		
		# Synth Lead (81-88)
		"lead_1_square": 80,
		"lead_2_sawtooth": 81,
		"lead_3_calliope": 82,
		"lead_4_chiff": 83,
		"lead_5_charang": 84,
		"lead_6_voice": 85,
		"lead_7_fifths": 86,
		"lead_8_bass_lead": 87,
		
		# Synth Pad (89-96)
		"pad_1_new_age": 88,
		"pad_2_warm": 89,
		"pad_3_polysynth": 90,
		"pad_4_choir": 91,
		"pad_5_bowed": 92,
		"pad_6_metallic": 93,
		"pad_7_halo": 94,
		"pad_8_sweep": 95,
		
		# Synth Effects (97-104)
		"fx_1_rain": 96,
		"fx_2_soundtrack": 97,
		"fx_3_crystal": 98,
		"fx_4_atmosphere": 99,
		"fx_5_brightness": 100,
		"fx_6_goblins": 101,
		"fx_7_echoes": 102,
		"fx_8_sci_fi": 103,
		
		# Ethnic (105-112)
		"sitar": 104,
		"banjo": 105,
		"shamisen": 106,
		"koto": 107,
		"kalimba": 108,
		"bagpipe": 109,
		"fiddle": 110,
		"shanai": 111,
		
		# Percussive (113-120)
		"tinkle_bell": 112,
		"agogo": 113,
		"steel_drums": 114,
		"woodblock": 115,
		"taiko_drum": 116,
		"melodic_tom": 117,
		"synth_drum": 118,
		"reverse_cymbal": 119,
		
		# Sound Effects (121-128)
		"guitar_fret_noise": 120,
		"breath_noise": 121,
		"seashore": 122,
		"bird_tweet": 123,
		"telephone_ring": 124,
		"helicopter": 125,
		"applause": 126,
		"gunshot": 127
	}

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

	def __add_effects(self, track, channel, effects):
		"""
		Add MIDI Control Change messages for effects
		
		Args:
			track: The MidiTrack to add effects to
			channel: MIDI channel
			effects: List of effect dictionaries
		"""
		if not effects:
			return
			
		for effect in effects:
			effect_type = effect.get("type")
			value = effect.get("value", 64)
			
			# Controller numbers for common effects
			controller_map = {
				"modulation": 1,
				"breath": 2,
				"volume": 7,
				"pan": 10,
				"expression": 11,
				"reverb": 91,
				"chorus": 93,
				"phaser": 95,
				"data_entry": 6,
				"sustain": 64,
				"resonance": 71,
				"release_time": 72,
				"attack_time": 73,
				"brightness": 74
			}
			
			if effect_type in controller_map:
				controller = controller_map[effect_type]
				track.append(Message('control_change', control=controller, 
								value=value, channel=channel, time=0))

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
				channel = note_data.get("channel", 0)
				
				# Create track key
				track_key = f"{instrument_name}_{channel}"
				
				# Create new track if needed
				if track_key not in instrument_tracks:
					track = MidiTrack()
					mid.tracks.append(track)
					instrument_tracks[track_key] = track
					
					# Set instrument program
					program_number = self.__INSTRUMENT_MAP.get(instrument_name, 0)
					track.append(Message('program_change', program=program_number, channel=channel, time=0))
				
				# Get the track
				track = instrument_tracks[track_key]

				self.__add_effects(track, channel=channel, effects=note_data.get("effects", "none"))
				
				# Process note
				note_duration = float(note_data.get("duration", 1.0))
				velocity = int(note_data.get("velocity", 64))
				ticks = int(self.__duration * note_duration)
				
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

	def generate_music(self, user_prompt, genre=None):
		"""
		Generate music based on user prompt and optionally specified genre
		
		Args:
			user_prompt: Text description of the desired music
			genre: Optional genre to guide the generation
		
		Returns:
			Path to generated WAV file
		"""
		# Add genre context if provided
		enhanced_prompt = user_prompt
		
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