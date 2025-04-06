class DrumKit:
    """
    A utility class to handle MIDI percussion (channel 10).
    Maps common drum names and aliases to MIDI note numbers.
    """
    _PRIMARY_MAP = {
        "acoustic_bass_drum": 35,
        "bass_drum": 36,
        "side_stick": 37,
        "acoustic_snare": 38,
        "hand_clap": 39,
        "electric_snare": 40,
        "low_floor_tom": 41,
        "closed_hi_hat": 42,
        "high_floor_tom": 43,
        "pedal_hi_hat": 44,
        "low_tom": 45,
        "open_hi_hat": 46,
        "low_mid_tom": 47,
        "hi_mid_tom": 48,
        "crash_cymbal_1": 49,
        "high_tom": 50,
        "ride_cymbal_1": 51,
        "chinese_cymbal": 52,
        "ride_bell": 53,
        "tambourine": 54,
        "splash_cymbal": 55,
        "cowbell": 56,
        "crash_cymbal_2": 57,
        "vibraslap": 58,
        "ride_cymbal_2": 59,
        "hi_bongo": 60,
        "low_bongo": 61,
        "mute_hi_conga": 62,
        "open_hi_conga": 63,
        "low_conga": 64,
    }

    _ALIASES = {
        "kick": "bass_drum",
        "kick_drum": "bass_drum",
        "snare": "acoustic_snare",
        "rimshot": "side_stick",
        "hh_closed": "closed_hi_hat",
        "hh_open": "open_hi_hat",
        "hh_pedal": "pedal_hi_hat",
        "tom_low": "low_tom",
        "tom_mid": "low_mid_tom",
        "tom_high": "high_tom",
        "crash": "crash_cymbal_1",
        "ride": "ride_cymbal_1",
        "chh": "closed_hi_hat",
        "ohh": "open_hi_hat",
        "clap": "hand_clap",
        "tamb": "tambourine",
        "conga_hi": "open_hi_conga",
        "conga_lo": "low_conga",
        "cow": "cowbell"
    }

    MIDI_CHANNEL = 9  # Channel 10 in MIDI spec

    @classmethod
    def get_midi_note(cls, name: str) -> int:
        """
        Get MIDI note number for a drum name or alias.

        Args:
            name (str): Drum sound name (e.g., 'kick', 'closed_hi_hat')

        Returns:
            int: MIDI note number or None if not found
        """
        name = name.lower()
        primary_name = cls._ALIASES.get(name, name)
        return cls._PRIMARY_MAP.get(primary_name)

    @classmethod
    def is_drum(cls, name: str) -> bool:
        """
        Check if a name is a valid drum sound or alias.

        Args:
            name (str): Name to check

        Returns:
            bool: True if it maps to a drum note
        """
        name = name.lower()
        return name in cls._PRIMARY_MAP or name in cls._ALIASES

    @classmethod
    def list_all(cls):
        """
        Print all available drum names and their MIDI numbers.
        """
        all_names = {**cls._PRIMARY_MAP, **{k: cls._PRIMARY_MAP[v] for k, v in cls._ALIASES.items()}}
        for name, midi_note in sorted(all_names.items(), key=lambda x: x[1]):
            print(f"{name:20} → {midi_note}")
