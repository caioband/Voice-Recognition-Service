import pyttsx3
import asyncio
import time

class Speaker:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.ShouldStop = False
        pass

    def OnSpeaking(self) -> None:
        if self.ShouldStop == True:
            self.engine.stop()
        pass

    async def Speak(self, settings, text: str) -> None:
        LANGUAGE = settings["language"]
        VOLUME = float(settings["volume"])/100
        voices = self.engine.getProperty('voices')
        language_audio = self.GetSpeaker(voices, LANGUAGE)

        self.engine.setProperty('voice', language_audio.id) #type: ignore
        self.engine.setProperty('volume', VOLUME)
        self.engine.say(text)
        self.engine.connect('started-word', self.OnSpeaking)
        self.engine.runAndWait()
        pass

    def Stop(self) -> None:
        print("Stopping")
        self.engine.stop()
        pass

    def identify_language_by_audio_name(self, name: str = "en-US"):
        if isinstance(name, str):
            if name.find('Portuguese') >= 0:
               return 'pt-BR'
            else:
                return 'en-US'

    def GetSpeaker(self, voice_objects, language: str = "en-US"):
        for i in voice_objects:
            language = self.identify_language_by_audio_name(i.name)
            if language == language:
                return i
        pass


