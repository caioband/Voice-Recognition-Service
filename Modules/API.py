from openai import OpenAI
import playsound
import dotenv
import os
import time



class API:
    def __init__(self, API_KEY: str) -> None:
        self.Client = OpenAI(api_key = API_KEY)
        pass
    def Chat(self, messages :list, temperature: float = 0.5, model: str = "gpt-3.5-turbo") -> str:
        response = self.Client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return str(response.choices[0].message.content)
    def Speak(self, input: str, voice = 'echo') -> None:
        response = self.Client.audio.speech.create(
            model="tts-1",
            voice = voice.lower(), # type: ignore
            input= input,
        )
        response.stream_to_file("./Cache/SpeechText.mp3")
        playsound.playsound("./Cache/SpeechText.mp3", True) # True = Yields code
        pass


dotenv.load_dotenv(dotenv.find_dotenv())

OPENAI_KEY = os.getenv("OPENAI_KEY")

