from mido import Message

class ControllerEffectKit:
	"""
	Utility class for MIDI controller/effect names (and aliases) to their control change numbers.
	Includes helpful methods and alias support.
	"""
	_CONTROLLERS = {
		# Bank
		"bank_select": 0,

		# Modulation and expression
		"modulation": 1, "mod_wheel": 1,
		"breath": 2, "breath_controller": 2,
		"foot_control": 4,
		"portamento": 5, "portamento_time": 5,
		"data_entry": 6,
		"volume": 7, "main_volume": 7, "channel_volume": 7,
		"balance": 8,
		"pan": 10,
		"expression": 11, "expression_controller": 11,

		# FX controls
		"effect1": 12, "fx1": 12, "reverb_level": 91,
		"effect2": 13, "fx2": 13, "chorus_level": 93,
		"tremolo": 92,
		"celeste": 94, "detune": 94,
		"phaser": 95,

		# General-purpose
		"general_1": 16,
		"general_2": 17,
		"general_3": 18,
		"general_4": 19,

		# Pedals & toggles
		"sustain": 64, "hold": 64,
		"portamento_toggle": 65,
		"sostenuto": 66,
		"soft_pedal": 67,
		"legato": 68,
		"hold_2": 69,

		# Sound controllers (synth control)
		"sound_ctrl_1": 70, "timbre": 70,
		"resonance": 71,
		"release_time": 72,
		"attack_time": 73,
		"brightness": 74,
		"sound_ctrl_6": 75,
		"sound_ctrl_7": 76,
		"sound_ctrl_8": 77,
		"sound_ctrl_9": 78,
		"sound_ctrl_10": 79,

		# Advanced control (NRPN/RPN)
		"data_increment": 96,
		"data_decrement": 97,
		"nrpn_lsb": 98,
		"nrpn_msb": 99,
		"rpn_lsb": 100,
		"rpn_msb": 101,

		# Channel mode messages
		"all_sound_off": 120,
		"reset_controllers": 121,
		"local_control": 122,
		"all_notes_off": 123,
		"omni_off": 124,
		"omni_on": 125,
		"mono_on": 126,
		"poly_on": 127
	}

	@classmethod
	def get_cc_number(cls, name: str) -> int:
		"""
		Get the MIDI control change number from the effect name or alias.
		Defaults to -1 if not found.
		"""
		name = name.lower()
		return cls._CONTROLLERS.get(name, -1)

	@classmethod
	def is_valid(cls, name: str) -> bool:
		name = name.lower()
		return name in cls._CONTROLLERS

	@staticmethod
	def add_effects(track, channel, note_data):
		"""
		Add MIDI Control Change messages for effects using ControllerMap
		
		Args:
			track: The MidiTrack to add effects to
			channel: MIDI channel
			effects: List of effect dictionaries
		"""
		effects = note_data.get("effects", None)
		if not effects:
			return

		for effect in effects:
			effect_type = effect.get("type")
			value = effect.get("value", 64)

			cc_number = ControllerEffectKit.get_cc_number(effect_type)
			if cc_number != -1:
				track.append(Message('control_change', control=cc_number, value=value, channel=channel, time=0))
