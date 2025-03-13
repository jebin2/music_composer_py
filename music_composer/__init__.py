from .main import MusicComposer

import os
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()