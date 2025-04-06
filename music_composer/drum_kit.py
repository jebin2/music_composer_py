class DrumKit:
    """
    A utility class to handle MIDI percussion (channel 10).
    Maps common drum names and aliases to MIDI note numbers.
    """
    _PRIMARY_MAP = {
        "bass_drum": 35,
        "acoustic_bass_drum": 35,
        "bass_drum_1": 36,
        "side_stick": 37,
        "acoustic_snare": 38,
        "hand_clap": 39,
        "electric_snare": 40,
        "low_floor_tom": 41,
        "closed_hihat": 42,
        "high_floor_tom": 43,
        "pedal_hihat": 44,
        "low_tom": 45,
        "open_hihat": 46,
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
        "high_timbale": 65,
        "low_timbale": 66,
        "high_agogo": 67,
        "low_agogo": 68,
        "cabasa": 69,
        "maracas": 70,
        "short_whistle": 71,
        "long_whistle": 72,
        "short_guiro": 73,
        "long_guiro": 74,
        "claves": 75,
        "hi_wood_block": 76,
        "low_wood_block": 77,
        "mute_cuica": 78,
        "open_cuica": 79,
        "mute_triangle": 80,
        "open_triangle": 81,
        "reverse_cymbal": 62
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
        return cls._PRIMARY_MAP.get(name)

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
        return name in cls._PRIMARY_MAP