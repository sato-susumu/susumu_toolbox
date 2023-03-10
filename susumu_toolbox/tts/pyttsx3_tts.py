import pyttsx3

from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.utility.config import Config


class Pyttsx3TTS(BaseTTS):
    def __init__(self, config: Config):
        super().__init__(config)
        self.engine = pyttsx3.init()

    def tts_play(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        pass

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass
