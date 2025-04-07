from setuptools import setup, find_packages

setup(
	name="music_composer",
	packages=find_packages(exclude=["tests*"]),
	package_data={
        "music_composer": ["system_prompt.txt", "GeneralUser-GS.sf2"]
    },
	install_requires=[
		"music21",
		"mido",
		"python-dotenv",
		"custom_logger @ git+https://github.com/jebin2/custom_logger.git",
		"gemiwrap @ git+https://github.com/jebin2/gemiwrap.git",
		"flask"
	],
	author="Jebin Einstein",
	description="Create music with Google's Gemini API.",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/jebin2/music_composer",  # Your repo URL
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",  # Choose a license
		"Operating System :: OS Independent",
	],
	python_requires=">=3.7",  # Specify minimum Python version
)