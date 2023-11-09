import speech_recognition as sr
import pyttsx3
import openai
import dotenv
import os
from termcolor import cprint

# language_choose = "en-US"
language_to_say = ''
dotenv.load_dotenv(dotenv.find_dotenv())

OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

def find_language_voice(voice_objects, language_choose: str = "en-US"):
    for i in voice_objects:
        language = identify_language_by_audio_name(i.name)
        if language == language_choose:
            return i


def speak_text(command, language: str = "en-US"):
    # print(command)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    language_audio = find_language_voice(voices, language)
    # id = getattr(language_audio, "id")

    engine.setProperty('voice', language_audio.id) #type: ignore
    engine.say(command)
    engine.runAndWait()

r = sr.Recognizer()


def record_text(language_choose: str ="en-US"):
    while .3:
        try:
            with sr.Microphone() as source2:
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                for i in voices:
                    current_index = identify_language_by_audio_name(i.name)
                    language_to_say = language_choose
                    if current_index == language_choose:
                        break

                r.adjust_for_ambient_noise(source2, duration=0.2) #type: ignore
                cprint("[VRS]: Listening to your microphone.", "green")
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2, language=language_to_say) #type: ignore
                return str(MyText).capitalize()
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))


def identify_language_by_audio_name(name):
    if isinstance(name, str):
        if name.find('Portuguese') >= 0:
           return 'pt-BR'
        else:
            return 'en-US'




def send_to_chatgpt(ms, model="gpt-3.5-turbo"):
    rp = openai.chat.completions.create(
        model=model,
        messages=ms,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = rp.choices[0].message.content
    ms.append(rp.choices[0].message)
    return message



##messages = []
##while 1:
##    text = record_text()
##    messages.append({"role": "user", "content": text})
##    response = send_to_chatgpt(messages)
##    speak_text(response)




##text = record_text()
##
##response = send_to_chatgpt([{"role": "user", "content": text}])
##speak_text(response)