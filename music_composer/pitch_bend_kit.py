import math
from mido import Message

class PitchEffectKit:
	"""
	Pitch Bend helper: mido expects -8192 to +8191
	"""
	MIN = -8192
	MAX = 8191

	@staticmethod
	def normalize(value: float) -> int:
		"""
		Convert -1.0 to 1.0 → -8192 to 8191
		"""
		return int(value * PitchEffectKit.MAX)

	@staticmethod
	def to_pitchwheel(value: float) -> int:
		"""Convert normalized float (-1.0 to 1.0) to pitchwheel value (-8192 to 8191)"""
		return PitchEffectKit.normalize(value) - PitchEffectKit.CENTER

	@staticmethod
	def get_pitch_values(note_data):
		if "pitch_bend" in note_data:
			bend = note_data["pitch_bend"]
			start = bend.get("start", 0.0)
			end = bend.get("end", 1.0)
			steps = bend.get("steps", 8)

			return bend, start, end, steps

		return None, None, None, None

	@staticmethod
	def add_pitch(track, channel, ticks, note_data):
		"""Add a glide from start to end bend over `ticks` duration"""

		bend, start, end, steps = PitchEffectKit.get_pitch_values(note_data)
		if bend:
			if steps <= 0:
				steps = 1
			step_ticks = ticks // steps
			for i in range(steps + 1):
				t = i / steps
				bend = start + (end - start) * t  # Linear interp
				pitch_val = PitchEffectKit.to_pitchwheel(bend)
				track.append(Message('pitchwheel', pitch=pitch_val, channel=channel, time=step_ticks if i > 0 else 0))

			# Reset to center
			track.append(Message('pitchwheel', pitch=0, channel=channel, time=0))

	@staticmethod
	def get_vib_values(note_data):
		if "vibrato" in note_data:
			vib = note_data["vibrato"]
			depth = vib.get("depth", 0.3)
			speed = vib.get("speed", 6)
			steps = vib.get("steps", 32)

			return vib, depth, speed, steps

		return None, None, None, None

	@staticmethod
	def add_vibrato(track, channel, ticks, note_data):
		"""Add vibrato: sinusoidal pitch modulation"""

		vib, depth, speed, steps = PitchEffectKit.get_pitch_values(note_data)
		if vib:
			if steps <= 0:
				steps = 1
			step_ticks = ticks // steps
			for i in range(steps + 1):
				t = i / steps
				bend = depth * math.sin(2 * math.pi * speed * t)
				pitch_val = PitchEffectKit.to_pitchwheel(bend)
				track.append(Message('pitchwheel', pitch=int(pitch_val), channel=channel, time=step_ticks if i > 0 else 0))

			# Reset to center
			track.append(Message('pitchwheel', pitch=0, channel=channel, time=0))