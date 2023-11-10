from datetime import datetime
import main
from regex import F
import requests
from sympy import content
from bs4 import BeautifulSoup
import threading
import json


async def WhatTimeIs():
    Time = datetime.now()
    return f"Now is {Time.hour}:{Time.minute} of {Time.day}/{Time.month}/{Time.year}"

async def CreateAlarm():
    return "Alarm created"

async def RemoveAlarm():
    return "Alarm removed"

async def SendMessage():
    return "Message sent"

# Possível
async def TellNews():
    # usa a api do discord, ela não vai retornar um html igual o g1
    RESPONSE = requests.get("https://g1.globo.com/") # vou fazer web scrapping, nao da pra fazer com o requests package
    CONTENT = RESPONSE.content # response.content = codigo em html
    site = BeautifulSoup(CONTENT, 'html.parser')
    noticias = site.findAll('div', attrs={'class': 'feed-post-body'})
    SETTINGS = json.loads(open("./settings/main.json", "r").read())
    IsVoiceEnabled = SETTINGS["voice"]
    Language = SETTINGS["language"]

    for noticia in noticias:
        titulo = noticia.find('a', attrs={'class': 'feed-post-link'})  #type: ignore
        if (IsVoiceEnabled):
            main.speak_text(titulo.text, Language)
        print(titulo.text) #type: ignore

        subtitulo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})

        if (subtitulo):
          if (IsVoiceEnabled):
            main.speak_text(subtitulo.text, Language)
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

async def RunCommand(commandName: str):
    CMDS = GetCommands()
    for Command in CMDS:
        if Command["name"] == commandName:
            return await Command["run"]()