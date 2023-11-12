from datetime import datetime
from numpy import number
from openai import audio
import random

from torch import seed
import main
from regex import F
import requests
from sympy import content
from bs4 import BeautifulSoup
from googletrans import Translator
from termcolor import cprint as print

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
    api.Speak(euIA[0])

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

            print(f"{pred_count,60-pred_one_min_count,(pred_count/(60-pred_one_min_count))}")
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
            print(f"{pred_count,60-pred_one_min_count,(pred_count/(60-pred_one_min_count))}")
            api.Speak(titulo.text)
            if (pred_count/(60-pred_one_min_count)) >= 0.14:
                content_translated = Languages.Translate(Settings,"Pausa de 30 segundos devido ao excesso de requests para a OpenAI, para pular essas interrupções, suporte-nos em nosso patreon!")
                print("Pausa de 30 segundos devido ao excesso de requests para a OpenAI, para pular essas interrupções, apoie-nos em nosso patreon!")
                api.Speak(content_translated)
                time.sleep(30)
                tts_count = 0
                one_min_count = 0
            ##api.Speak(titulo.text)

    return titulo.text #type: ignore

def OrderFood():
    return "Food ordered"

def CreateText(Settings):
    Inputs=[
        "Please, Describe the text you want me to create.",
        "Describe the text you want me to create.",
        "Tell-me how the text should be written.",
        "I need you to describe the text you want me to create.",
        "I need more details about the text you want me to create.",
    ]
    Input_Choice = random.choice(Inputs)
    content_translated = Languages.Translate(Settings,Input_Choice)
    print(f"[VRS]: {content_translated}", "cyan")
    api.Speak(content_translated)

    text_details = main.record_text(Settings['language'])
    print(str(text_details))

    api_responses = api.Chat(messages=[
        {"role": "system", "content": "Interprete o pedido do usuário considerando: erros de linguagem, erros de sintaxe, apenas ignore-os"},
        {"role": "system", "content": "Crie um passo a passo de intruções para a criação do texto."},
        {"role": "system", "content": "Identifique ou crie parametros como: 'title' sendo o título do texto, crie um nome de arquivo sem a extensão de arquivo, 'task' sendo a tarefa, 'author' sendo o criador, 'language' sendo a lingua, com base nas instruções do usuário"},
        {"role": "system", "content": "Crie um objeto JSON com os parametros identificados, e retorne o objeto JSON"},
        {"role": "user", "content": text_details}
    ])
    api_response = json.loads(api_responses[0])

    Text_Title = api_response["title"]
    Text_Task = api_response["task"]
    Text_Author = api_response["author"]
    Text_Language = api_response["language"]

    Responses = api.Chat(messages=[
        {"role": "system", "content": "É extremamente importante que sua resposta utilize somente de caracteres alfanuméricos. (exemplo: 'a-z', '0-9', 'A-Z')"},
        {"role": "system", "content": f"Você é um escrito de redações no modelo ENEM e deve criar um texto de acordo com as normas do ENEM"},
        {"role": "system", "content": "Interprete a tarefa a ser executada e crie o texto solicitado."},
        {"role": "system", "content": "O texto será inserido diretamente em um arquivo, e deve estar pronto para que seja executado, sem alterações, entenda que, não pode-se acrescentar nada além de texto na sua resposta."},
        {"role": "user", "content": f"Crie uma redação no modelo do ENEM, com o tema: {Text_Task} na linguagem: {Text_Language}. O texto deve ser escrito por: {Text_Author}."},
    ], temperature=0.5, tokens=1250)

    Response_Text = Responses[0]
    Path = f"{os.path.expanduser('~')}\\Documents\\{Text_Title}.txt"
    with open(Path, "w", encoding='utf-8') as f:
        f.write(str(Response_Text))
        print(f"[VRS]: Text created: {Text_Title}", "cyan")
    os.system('notepad.exe + "Path"')

    # Fale o titulo, conteudo, autor, e a lingua do texto
    input = f"I wrote the text about: {Text_Task}. in {Text_Language}."
    translated = Languages.Translate(Settings, input)
    api.Speak(translated)

    pass

def CreateNewCode(Settings):
    api_response = "None"

    Inputs=[
        "Please, Describe the code you want me to create.",
        "Describe the code you want me to create.",
        "Tell-me how the code should be written.",
        "I need you to describe the code you want me to create.",
        "I need more details about the code you want me to create.",
    ]
    Input_Choice = random.choice(Inputs)
    content_translated = Languages.Translate(Settings,Input_Choice)
    print(f"[VRS]: {content_translated}", "cyan")
    api.Speak(content_translated)

    code_details = main.record_text(Settings['language'])
    print(str(code_details))

    api_response = api.Chat(messages=[
        {"role": "system", "content": "Interprete o pedido do usuário considerando: erros de linguagem, erros de sintaxe, apenas ignore-os"},
        {"role": "system", "content": "Identifique o que o usuário quer que você faça e em qual linguagem de programação"},
        {"role": "system", "content": "Se o usuário não especificar nenhuma linguagem de programação conhecida na frase, interprete uma linguagem de programação que poderia se adaptar ao pedido do usuário, caso contrário, retorne a mensagem como um objeto JSON, sem nenhum tipo de texto além disso, indexando no objeto oque o usuário pediu, em qual linguagem de programação ele quer, o nome do arquivo deverá ser criado com base no contexto do pedido e a extensão do arquivo da linguagem de programação que o usuário pediu, (exemplo: '.js')"},
        {"role": "system", "content": "Indexe nesse JSON; crie etapas de acordo com o que o usuário pediu em formato de texto e indexe como: 'task', a linguagem de programação selecionada como: 'p_language', defina a criatividade necessária para a tarefa em escala de (0-2) como 'temperature', o nome do arquivo como 'file_name' sem a extensão do arquivo, e a extensão do arquivo como 'ext'"},
        {"role": "user", "content": code_details}],
        temperature=0.5,
        tokens=1250,
    )

    print(api_response[0])

    api_response = json.loads(api_response[0])

    Project_Language = api_response["p_language"]
    Project_Task = api_response["task"]
    Project_Temperature = api_response["temperature"]
    Project_FileName = api_response["file_name"]

    Responses = api.Chat(messages=[
        {"role": "system", "content": "É extremamente importante que sua resposta utilize somente de caracteres alfanuméricos. (exemplo: 'a-z', '0-9', 'A-Z')"},
        {"role": "system", "content": f"Imagine que você está dentro de um interpretador de código na linguagem: {Project_Language} e que deve responder de acordo com a normas da linguagem de programação."},
        {"role": "system", "content": "Interprete a tarefa a ser executada e crie o código solicitado."},
        {"role": "system", "content": "O código será inserido diretamente em um arquivo, e deve estar pronto para que seja executado, sem alterações, entenda que, não pode-se acrescentar nada além de código na sua resposta."},
        {"role": "system", "content": "Interprete o código criado, Crie comentários no código utilizando o sistema de comentários da linguagem de programação que o usuário pediu, explicando o que cada parte do código faz, e o que o código faz como um todo, e retorne o código com os comentários"},
        {"role": "system", "content": "Retorne somente o código, é importante que não contenha nenhum tipo de texto além do código, não é necessário que utilize de markdown ou formatações do tipo, apenas o código."},
        {"role": "system", "content": "Não crie instruções, comentários que não estejam em formato de código, e não insira caracteres que não sejam alfanuméricos, (exemplo: 'a-z', '0-9', 'A-Z')"},
        {"role": "user", "content": f"{Project_Task} ({Project_Language})"}],
        temperature=float(Project_Temperature),
        tokens=2000,
    )

    time = datetime.now()
    extension = api_response["ext"]
    with open(f"./scripts/{Project_FileName}{extension}", 'w', encoding='utf-8') as f:
        f.write(str(Responses[0]))
        print(f"[VRS]: Code created: {Project_FileName}{extension}", "cyan")
        codePath = os.path.abspath(f"./scripts/{Project_FileName}{extension}")
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
        "name": "What is your name",
        "run": IntroduceYourself,
    },
    {
        "name": "Introduce yourself",
        "run": IntroduceYourself,
    },
    {
        "name": "What you can do?",
        "run": IntroduceYourself,
    },
    {
        "name": "Write code",
        "run": CreateNewCode,
    },
    {
        "name": "Write text",
        "run": CreateText,
    }
]

def GetCommands():
    return Commands

def RunCommand(commandName: str, Settings):
    CMDS = GetCommands()
    for Command in CMDS:
        if Command["name"] == commandName:
            return Command["run"](Settings)