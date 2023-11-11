from datetime import datetime
from numpy import number
from openai import audio

from torch import seed
import main
from regex import F
import requests
from sympy import content
from bs4 import BeautifulSoup
from googletrans import Translator

import os
import dotenv
import Modules.API as API
import Modules.Languages as languages
import Sentence
import threading
import json
import time

dotenv.load_dotenv(dotenv.find_dotenv())

OPENAI_KEY = os.getenv("OPENAI_KEY")

api = API.API(OPENAI_KEY) #type: ignore

Languages = languages.Translator()

STS = Sentence.SentenceService()

def identify_alarm_hour_by_str(text : str):
    Alarm = []
    final_string = ''
    for i in text:
        if i.isnumeric():
            Alarm.append(i)

    for i in range(len(Alarm)):
        if i <= 1:
            final_string = Alarm[0] + Alarm[1]
        else:
            final_string += Alarm[i]

    return final_string


def WhatTimeIs(Settings):
    Time = datetime.now()
    return f"Now is {Time.hour}:{Time.minute} of {Time.day}/{Time.month}/{Time.year}"

def CreateAlarm(Settings):
    audiotext = Languages.Translate(Settings, "For what time would you like to set?")

    api.Speak(audiotext)
    #main.speak_text(audiotext, Settings["language"], Settings["volume"])
    speak_alarm_hour = main.record_text(Settings["language"])

    final_string = identify_alarm_hour_by_str(speak_alarm_hour) #type: ignore

    final_string = final_string[:2] + ':' + final_string[2:]

    print(final_string)
    return "Alarm created"

def RemoveAlarm():
    return "Alarm removed"

def SendMessage():
    return "Message sent"

# Possível

def IntroduceYourself(Settings):
    content_translated = Languages.Translate(Settings,"Apresente-se para o mundo")
    euIA = api.Chat([
    {"role": "system", "content": "Você é um assistente virtual que usa a API da OpenAI e que está em desenvolvimento pelo Caio Bandeira e o João Teixeira, mais conhecido como 'SinceVoid'"},
    {"role": "system", "content": "Atualmente você suporta apenas as linguagens em português e inglês"},
    {"role": "system", "content": "Está sendo desenvolvido para auxiliar tanto em perguntas por voz e texto, mas também para, futuramente, poder facilitar as suas interações dentro de casa e com o mundo"},
    {"role": "user", "content": content_translated}])
    api.Speak(euIA)

def TellNews(Settings):
    RESPONSE = requests.get("https://g1.globo.com/")
    CONTENT = RESPONSE.content # response.content = codigo em html
    site = BeautifulSoup(CONTENT, 'html.parser')
    noticias = site.findAll('div', attrs={'class': 'feed-post-body'})
    IsVoiceEnabled = Settings["voice"]
    Language = Settings["language"]
    Volume = Settings["volume"]

    for noticia in noticias:
        titulo = noticia.find('a', attrs={'class': 'feed-post-link'})  #type: ignore
        if (IsVoiceEnabled):
            time.sleep(1)
            api.Speak(titulo.text)
            #main.speak_text(titulo.text, Language, Volume/100)
        print(titulo.text) #type: ignore

        subtitulo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})

        if (subtitulo):
          if (IsVoiceEnabled):
            time.sleep(1)
            api.Speak(subtitulo.text)
            #main.speak_text(subtitulo.text, Language, Volume/100)
            print(subtitulo.text)

    return titulo.text #type: ignore

def OrderFood():
    return "Food ordered"

Commands = [
    {
        "name": "What time is?",
        "run": WhatTimeIs
    },
    {
        "name": "Create an alarm",
        "run": CreateAlarm,
    },
    {
        "name": "Send a message",
        "run": SendMessage,
    },
    {
        "name": "News of the day",
        "run": TellNews,
    },
    {
        "name": "Order food",
        "run": OrderFood,
    },
    {
        "name": "Who are you",
        "run": IntroduceYourself,
    },
]

def GetCommands():
    return Commands

def RunCommand(commandName: str, Settings):
    CMDS = GetCommands()
    for Command in CMDS:
        if Command["name"] == commandName:
            return Command["run"](Settings)