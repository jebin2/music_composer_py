from music21 import instrument
import inspect

class InstrumentKit:
    """
    Utility class for instrument names (and aliases) to MIDI program numbers.
    Includes support for common aliases and listing capabilities.
    """

    def __init__(self):
        self.INSTRUMENTS = {
            "acoustic_grand": {"midi_program": 0},
            "bright_acoustic": {"midi_program": 1},
            "electric_grand": {"midi_program": 2},
            "honky_tonk": {"midi_program": 3},
            "electric_piano_1": {"midi_program": 4},
            "electric_piano_2": {"midi_program": 5},
            "harpsichord": {"midi_program": 6},
            "clavinet": {"midi_program": 7},
            "celesta": {"midi_program": 8},
            "glockenspiel": {"midi_program": 9},
            "music_box": {"midi_program": 10},
            "vibraphone": {"midi_program": 11},
            "marimba": {"midi_program": 12},
            "xylophone": {"midi_program": 13},
            "tubular_bells": {"midi_program": 14},
            "dulcimer": {"midi_program": 15},
            "drawbar_organ": {"midi_program": 16},
            "percussive_organ": {"midi_program": 17},
            "rock_organ": {"midi_program": 18},
            "church_organ": {"midi_program": 19},
            "reed_organ": {"midi_program": 20},
            "accordion": {"midi_program": 21},
            "harmonica": {"midi_program": 22},
            "tango_accordion": {"midi_program": 23},
            "acoustic_guitar_nylon": {"midi_program": 24},
            "acoustic_guitar_steel": {"midi_program": 25},
            "electric_guitar_jazz": {"midi_program": 26},
            "electric_guitar_clean": {"midi_program": 27},
            "electric_guitar_muted": {"midi_program": 28},
            "overdriven_guitar": {"midi_program": 29},
            "distortion_guitar": {"midi_program": 30},
            "guitar_harmonics": {"midi_program": 31},
            "acoustic_bass": {"midi_program": 32},
            "electric_bass_finger": {"midi_program": 33},
            "electric_bass_pick": {"midi_program": 34},
            "fretless_bass": {"midi_program": 35},
            "slap_bass_1": {"midi_program": 36},
            "slap_bass_2": {"midi_program": 37},
            "synth_bass_1": {"midi_program": 38},
            "synth_bass_2": {"midi_program": 39},
            "violin": {"midi_program": 40},
            "viola": {"midi_program": 41},
            "cello": {"midi_program": 42},
            "contrabass": {"midi_program": 43},
            "tremolo_strings": {"midi_program": 44},
            "pizzicato_strings": {"midi_program": 45},
            "orchestral_harp": {"midi_program": 46},
            "timpani": {"midi_program": 47},
            "string_ensemble_1": {"midi_program": 48},
            "string_ensemble_2": {"midi_program": 49},
            "synth_strings_1": {"midi_program": 50},
            "synth_strings_2": {"midi_program": 51},
            "choir_aahs": {"midi_program": 52},
            "voice_oohs": {"midi_program": 53},
            "synth_choir": {"midi_program": 54},
            "orchestra_hit": {"midi_program": 55},
            "trumpet": {"midi_program": 56},
            "trombone": {"midi_program": 57},
            "tuba": {"midi_program": 58},
            "muted_trumpet": {"midi_program": 59},
            "french_horn": {"midi_program": 60},
            "brass_section": {"midi_program": 61},
            "synth_brass_1": {"midi_program": 62},
            "synth_brass_2": {"midi_program": 63},
            "soprano_sax": {"midi_program": 64},
            "alto_sax": {"midi_program": 65},
            "tenor_sax": {"midi_program": 66},
            "baritone_sax": {"midi_program": 67},
            "oboe": {"midi_program": 68},
            "english_horn": {"midi_program": 69},
            "bassoon": {"midi_program": 70},
            "clarinet": {"midi_program": 71},
            "piccolo": {"midi_program": 72},
            "flute": {"midi_program": 73},
            "recorder": {"midi_program": 74},
            "pan_flute": {"midi_program": 75},
            "blown_bottle": {"midi_program": 76},
            "shakuhachi": {"midi_program": 77},
            "whistle": {"midi_program": 78},
            "ocarina": {"midi_program": 79},
            "lead_1_square": {"midi_program": 80},
            "lead_2_sawtooth": {"midi_program": 81},
            "lead_3_calliope": {"midi_program": 82},
            "lead_4_chiff": {"midi_program": 83},
            "lead_5_charang": {"midi_program": 84},
            "lead_6_voice": {"midi_program": 85},
            "lead_7_fifths": {"midi_program": 86},
            "lead_8_bass_lead": {"midi_program": 87},
            "pad_1_new_age": {"midi_program": 88},
            "pad_2_warm": {"midi_program": 89},
            "pad_3_polysynth": {"midi_program": 90},
            "pad_4_choir": {"midi_program": 91},
            "pad_5_bowed": {"midi_program": 92},
            "pad_6_metallic": {"midi_program": 93},
            "pad_7_halo": {"midi_program": 94},
            "pad_8_sweep": {"midi_program": 95},
            "fx_1_rain": {"midi_program": 96},
            "fx_2_soundtrack": {"midi_program": 97},
            "fx_3_crystal": {"midi_program": 98},
            "fx_4_atmosphere": {"midi_program": 99},
            "fx_5_brightness": {"midi_program": 100},
            "fx_6_goblins": {"midi_program": 101},
            "fx_7_echoes": {"midi_program": 102},
            "fx_8_sci_fi": {"midi_program": 103},
            "sitar": {"midi_program": 104},
            "banjo": {"midi_program": 105},
            "shamisen": {"midi_program": 106},
            "koto": {"midi_program": 107},
            "kalimba": {"midi_program": 108},
            "bagpipe": {"midi_program": 109},
            "fiddle": {"midi_program": 110},
            "shanai": {"midi_program": 111},
            "tinkle_bell": {"midi_program": 112},
            "agogo": {"midi_program": 113},
            "steel_drums": {"midi_program": 114},
            "woodblock": {"midi_program": 115},
            "taiko_drum": {"midi_program": 116},
            "melodic_tom": {"midi_program": 117},
            "synth_drum": {"midi_program": 118},
            "reverse_cymbal": {"midi_program": 119},
            "guitar_fret_noise": {"midi_program": 120},
            "breath_noise": {"midi_program": 121},
            "seashore": {"midi_program": 122},
            "bird_tweet": {"midi_program": 123},
            "telephone_ring": {"midi_program": 124},
            "helicopter": {"midi_program": 125},
            "applause": {"midi_program": 126},
            "gunshot": {"midi_program": 127}
        }


        for name, cls in inspect.getmembers(instrument, inspect.isclass):
            if issubclass(cls, instrument.Instrument) and cls is not instrument.Instrument:
                inst = cls()
                if inst.midiProgram is not None:
                    # Normalize the name to lowercase with underscores (e.g. "AcousticBass" -> "acoustic_bass")
                    normalized_name = ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
                    if normalized_name not in self.INSTRUMENTS:
                        self.INSTRUMENTS[normalized_name] = {
                            "midi_program": inst.midiProgram
                        }

                    self.INSTRUMENTS[normalized_name]["class"]= cls

        for key, val in self.INSTRUMENTS.items():
            if not "class" in val:
                midi_program = val["midi_program"]
                for inner_key, inner_val in self.INSTRUMENTS.items():
                    if "class" in inner_val and inner_val["midi_program"] == midi_program:
                        val["class"] = inner_val["class"]
                        break

            if not "class" in val:
                val["class"] = instrument.MIDI_PROGRAM_TO_INSTRUMENT[midi_program]

    def get_midi_map(self):
        return {key: val["midi_program"] for key, val in self.INSTRUMENTS.items()}

    def get_class_map(self):
        return {key: val["class"] for key, val in self.INSTRUMENTS.items()}

    def get_program_number(self, name: str) -> int:
        """
        Get the MIDI program number from an instrument name or alias.
        Defaults to 0 (acoustic_grand) if not found.
        """
        name = name.lower()
        return self.INSTRUMENTS.get(name, {}).get("midi_program", 0)

    def is_valid(self, name: str) -> bool:
        return name.lower() in self.INSTRUMENTS
