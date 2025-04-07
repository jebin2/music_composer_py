import os
from music21 import stream, note, tempo, meter, key, instrument
from .instrument_kit import InstrumentKit
import json
from .drum_kit import DrumKit

def image_notes(music_data_path, output_path):
    try:
        with open(music_data_path, "r") as f:
            music_data = json.load(f)

        # Create the score
        score = stream.Score()

        # Parse global metadata
        ks = key.Key(music_data["key_signature"])
        ts = meter.TimeSignature(music_data["time_signature"])
        tempo_mark = tempo.MetronomeMark(number=music_data["tempo"])

        # Create parts indexed by channel
        parts_by_channel = {}

        inst_kit = InstrumentKit()

        # Build parts dynamically
        for note_dict in music_data["notes"]:
            ch = note_dict["channel"]
            instr_name = note_dict["instrument"]

            if ch not in parts_by_channel:
                if ch == 9:
                    midi_program = DrumKit._PRIMARY_MAP.get(instr_name)
                    class_inst = instrument.MIDI_PROGRAM_TO_INSTRUMENT[midi_program]()
                else:
                    class_inst = inst_kit.get_class_map()[instr_name]()

                part = stream.Part()
                part.insert(0, class_inst)
                part.insert(0, ks)
                part.insert(0, ts)
                part.insert(0, tempo_mark)
                parts_by_channel[ch] = part

            # Create and insert note
            n = note.Note(note_dict["pitch"])
            n.duration.quarterLength = note_dict["duration"]
            n.volume.velocity = note_dict["velocity"]
            parts_by_channel[ch].insert(note_dict["offset"], n)

        # Add parts to score
        for part in parts_by_channel.values():
            score.insert(0, part)

        # Write to PNG using LilyPond
        score.write('lily.png', fp=output_path)

        # Remove extra files created by LilyPond (if they exist)
        for ext in ["", "-1.eps", "-2.eps", "-3.eps", "-systems.count", "-systems.tex", "-systems.texi"]:
            path = f"{output_path}{ext}"
            if os.path.exists(path):
                os.remove(path)

    except:
        pass
