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


import Build.Languages as languages
import Sentence
import threading
import json

Languages = languages.Translator()

STS = Sentence.SentenceService()

def identify_alarm_hour_by_str(text : str):
    Alarm = []
    for i in text:
        if i.isnumeric():
            Alarm.append(i)
    return Alarm


async def WhatTimeIs(Settings):
    Time = datetime.now()
    return f"Now is {Time.hour}:{Time.minute} of {Time.day}/{Time.month}/{Time.year}"

async def CreateAlarm(Settings):
    audiotext = Languages.Translate(Settings, "For what time would you like to set?")
    main.speak_text(audiotext, Settings["language"], Settings["volume"])
    speak_alarm_hour = main.record_text(Settings["language"])
    print(identify_alarm_hour_by_str(speak_alarm_hour)) #type: ignore
    return "Alarm created"

async def RemoveAlarm():
    return "Alarm removed"

async def SendMessage():
    return "Message sent"

# Possível
async def TellNews(Settings):
    # usa a api do discord, ela não vai retornar um html igual o g1
    RESPONSE = requests.get("https://g1.globo.com/") # vou fazer web scrapping, nao da pra fazer com o requests package
    CONTENT = RESPONSE.content # response.content = codigo em html
    site = BeautifulSoup(CONTENT, 'html.parser')
    noticias = site.findAll('div', attrs={'class': 'feed-post-body'})
    IsVoiceEnabled = Settings["voice"]
    Language = Settings["language"]
    Volume = Settings["volume"]

    for noticia in noticias:
        titulo = noticia.find('a', attrs={'class': 'feed-post-link'})  #type: ignore
        if (IsVoiceEnabled):
            main.speak_text(titulo.text, Language, Volume/100)
        print(titulo.text) #type: ignore

        subtitulo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})

        if (subtitulo):
          if (IsVoiceEnabled):
            main.speak_text(subtitulo.text, Language, Volume/100)
            print(subtitulo.text)

    return titulo.text #type: ignore

async def OrderFood():
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
]

def GetCommands():
    return Commands

async def RunCommand(commandName: str, Settings):
    CMDS = GetCommands()
    for Command in CMDS:
        if Command["name"] == commandName:
            return await Command["run"](Settings)