from openai import OpenAI
import playsound
import dotenv
import os
import time



class API:
    def __init__(self, API_KEY: str) -> None:
        self.Client = OpenAI(api_key = API_KEY)
        pass
    def Chat(self, messages :list, temperature: float = 0.5, tokens: int = 900, model: str = "gpt-3.5-turbo", responses: int = 1) -> list:
        response = self.Client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=tokens,
            n=responses
        )
        ai_responses = []
        for choice in response.choices:
            ai_responses.append(choice.message.content)
        return ai_responses
    def Speak(self, input: str, voice = 'echo') -> None:
        response = self.Client.audio.speech.create(
            model="tts-1",
            voice = voice.lower(), # type: ignore
            input= input,
        )
        response.stream_to_file("./Cache/SpeechText.mp3")
        playsound.playsound("./Cache/SpeechText.mp3", True) # True = Yields code

        if os.path.exists("./Cache/SpeechText.mp3"):
            os.remove("./Cache/SpeechText.mp3")
        pass



