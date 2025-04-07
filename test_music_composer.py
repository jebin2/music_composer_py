from music_composer import MusicComposer

musicComposer = MusicComposer()

music_data = None

jazz_file = musicComposer.generate_music("""Create atleast 30 second music: **Panel 1: Top Left \<cat 1(male)\>:**
"Did you ever wonder what we'd do if we suddenly grew opposable thumbs overnight?"

**Panel 2: Top Right \<cat 2(female)\>:**
"Open our own food cans, obviously. No more waiting for humans to wake up."

**Panel 3: Bottom Left \<cat 1(male)\>:**
"Think bigger! We could text our humans when they're late coming home with dinner."

**Panel 4: Bottom Right \<cat 2(female)\>:**
"Or unlock doors... imagine the neighborhood chaos with all cats free to roam!"

## Page 2:
**Panel 1: Top Left \<cat 1(male)\>:**
"We could finally figure out how the laser pointer works and control it ourselves!"

**Panel 2: Top Right \<cat 2(female)\>:**
"Wait—we could take selfies while our humans are sleeping and post them online!"

**Panel 3: Bottom Left \<cat 1(male)\>:**
"World domination would be just a thumb-click away..."

**Panel 4: Bottom Right \<cat 2(female)\>:**
"Let's be honest—we'd still just knock things off shelves, but with better precision."""
, music_data=music_data)