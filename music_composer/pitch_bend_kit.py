class PitchBendKit:
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
		return int(value * PitchBendKit.MAX)
