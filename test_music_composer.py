from music_composer import MusicComposer

musicComposer = MusicComposer()

music_data = None

jazz_file = musicComposer.generate_music("""## When Aliens Return Your Socks

### Page 1:
**Panel 1: Top Left** \<Alex (male)\>: "Did you know that aliens have been stealing our missing socks for decades?"

**Panel 2: Top Right** \<Maya (female)\>: "Wait, what? Is that why I only have mismatched pairs?"

**Panel 3: Bottom Left** \<Alex (male)\>: "Exactly! They've been using them as fuel for their spaceships—they convert cotton to cosmic energy."

**Panel 4: Bottom Right** \<Maya (female)\>: "So THAT'S why the weirdest ones always disappear first. The aliens have fashion sense!"

### Page 2:
**Panel 1: Top Left** \<Alex (male)\>: "The thing is, they've decided to return them all next Tuesday. ALL of them. Every missing sock since 1952."

**Panel 2: Top Right** \<Maya (female)\>: "Oh no...that's millions of socks! Where will we put them all?"

**Panel 3: Bottom Left** \<Alex (male)\>: "The aliens suggest we build sock pyramids. They say it's what they did on their planet."

**Panel 4: Bottom Right** \<Maya (female)\>: "Great. First global warming, now global sock-warming. The apocalypse is getting really weird."""
, music_data=music_data)