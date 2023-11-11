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
from termcolor import cprint

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
    euIA = api.Chat(messages=[
    {"role": "system", "content": "Você é um assistente virtual que usa a API da OpenAI e que está em desenvolvimento pelo Caio Bandeira e o João Teixeira, mais conhecido como 'SinceVoid'"},
    {"role": "system", "content": "Atualmente suporta apenas as linguagens em português e inglês"},
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
    one_min_count = 0
    tts_count = 0
    for noticia in noticias:
        titulo = noticia.find('a', attrs={'class': 'feed-post-link'})  #type: ignore
            #main.speak_text(titulo.text, Language, Volume/100)
         #type: ignore

        subtitulo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})

        if (subtitulo):
          if (IsVoiceEnabled):
            time.sleep(5)
            one_min_count += 5
            tts_count += 1
            pred_one_min_count = one_min_count + 5
            pred_count = tts_count + 1
            print('noticia' + " " + str(tts_count))
            print(titulo.text + '/' + subtitulo.text)
            print(pred_count,60-pred_one_min_count,(pred_count/(60-pred_one_min_count)))
            api.Speak(titulo.text + ',' + subtitulo.text)
            if (pred_count/(60-pred_one_min_count)) >= 0.2:
                content_translated = Languages.Translate(Settings,"Pausa de 30 segundos devido ao excesso de requests para a OpenAI, para pular essas interrupções, suporte-nos em nosso patreon!")
                api.Speak(content_translated)
                print("Pausa de 30 segundos devido ao excesso de requests para a OpenAI, para pular essas interrupções, suporte-nos em nosso patreon!")
                time.sleep(30)
                tts_count = 0
                one_min_count = 0
            #main.speak_text(subtitulo.text, Language, Volume/100)
        else:
            time.sleep(5)
            one_min_count += 5
            tts_count += 1
            pred_one_min_count = one_min_count + 5
            pred_count = tts_count + 1
            print('noticia' + " " + str(tts_count))
            print(titulo.text)
            print(pred_count,60-pred_one_min_count,(pred_count/(60-pred_one_min_count)))
            api.Speak(titulo.text)
            if (pred_count/(60-pred_one_min_count)) >= 0.14:
                content_translated = Languages.Translate(Settings,"Pausa de 30 segundos devido ao excesso de requests para a OpenAI, para pular essas interrupções, suporte-nos em nosso patreon!")
                print("Pausa de 30 segundos devido ao excesso de requests para a OpenAI, para pular essas interrupções, suporte-nos em nosso patreon!")
                api.Speak(content_translated)
                time.sleep(30)
                tts_count = 0
                one_min_count = 0
            ##api.Speak(titulo.text)

    return titulo.text #type: ignore

def OrderFood():
    return "Food ordered"

def CreateNewCode(Settings):
    api_response = "None"
    content_translated = Languages.Translate(Settings,"Por favor, diga-me com mais detalhes o código que você gostaria que eu fizesse.")
    api.Speak(content_translated)

    code_details = main.record_text(Settings['language'])
    print(code_details)

    api_response = api.Chat(messages=[
        {"role": "system", "content": "Identifique o que o usuário quer que você faça e em qual linguagem de programação"},
        {"role": "system", "content": "Se o usuário não especificar nenhuma linguagem de programação conhecida na frase, retorne apenas 'None',caso contrário, retorne a mensagem como um objeto JSON,sem nenhum tipo de texto além disso, indexando no objeto o que o usuário pediu, em qual linguagem de programação ele quer e a extensão do arquivo da linguagem de programação que o usuário pediu(exemplo: '.js')"},
        {"role": "system", "content": "Indexe o que o usuário pediu como 'To_do', a linguagem que ele quer como 'p_language'e a extensão do arquivo como 'ext'"},
        {"role": "user", "content": code_details}],
        temperature=0
    )

    print(api_response)

    api_response = json.loads(api_response)




    content_translated = Languages.Translate(Settings,api_response["To_do"] + " em " + api_response["p_language"])

    #
    final_code = api.Chat(messages=[
        {"role": "system", "content": "responda apenas com o código que o usuário pediu, sem nenhum tipo de texto além disso"},
        {"role": "user", "content": content_translated}
        ], temperature=1)

    time = datetime.now()
    fileDate = f"{time.day}_{time.month}_{time.year}-{time.hour}-{time.minute}-{time.second}"
    fileName = f"code_{fileDate}"
    extension = api_response["ext"]
    with open(f"./scripts/{fileName}{extension}", 'w', encoding='utf-8') as f:
        f.write(str(final_code))
        cprint(f"[VRS]: Code created: {fileName}{extension}", "cyan")
        codePath = os.path.abspath(f"./scripts/{fileName}{extension}")
        os.system(f'code "{codePath}"')

    return

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
    {
        "name": "New code",
        "run": CreateNewCode,
    },
]

def GetCommands():
    return Commands

def RunCommand(commandName: str, Settings):
    CMDS = GetCommands()
    for Command in CMDS:
        if Command["name"] == commandName:
            return Command["run"](Settings)