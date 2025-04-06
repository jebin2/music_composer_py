class ControllerKit:
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

    _ALIASES = {
        "mod_wheel": "modulation",
        "main_volume": "volume",
        "hold": "sustain",
        "attack": "attack_time",
        "release": "release_time",
        "expr": "expression",
        "reverb_level": "reverb",
        "chorus_level": "chorus",
        "panpot": "pan"
    }

    @classmethod
    def get_cc_number(cls, name: str) -> int:
        """
        Get the MIDI control change number from the effect name or alias.
        Defaults to -1 if not found.
        """
        name = name.lower()
        resolved = cls._ALIASES.get(name, name)
        return cls._CONTROLLERS.get(resolved, -1)

    @classmethod
    def is_valid(cls, name: str) -> bool:
        name = name.lower()
        return name in cls._CONTROLLERS or name in cls._ALIASES

    @classmethod
    def list_all(cls):
        """
        Print all controller names and their CC numbers.
        Includes aliases with their mapped values.
        """
        combined = {**cls._CONTROLLERS, **{k: cls._CONTROLLERS[v] for k, v in cls._ALIASES.items()}}
        for name, cc in sorted(combined.items(), key=lambda x: x[1]):
            print(f"{name:20} → CC {cc}")
