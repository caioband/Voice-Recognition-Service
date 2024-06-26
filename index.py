import os as System
from os import system as Shell
from os import getenv as Env
from datetime import datetime as Date
import main
from termcolor import cprint as print
import Sentence
import Commands
import json
from dotenv import load_dotenv as LoadDotEnv, find_dotenv as FindDotEnv
from pymsgbox import alert as msg
import PySimpleGUI as sg

LoadDotEnv(FindDotEnv())

# Modules
import Modules.Languages as LanguageBuilder
import Modules.Speaker as SpeakerBuilder
from Modules.API import API

OpenAI = API(
    API_KEY=str(Env("OPENAI_KEY")),
) #type: ignore

STS = Sentence.SentenceService()
##CMDS = Commands.GetCommands()

# PyGui
rowSize = (50, 2)
btnSize = (int(rowSize[0]/3), rowSize[1])
CodingLanguages = [
    "Python",
    "JavaScript",
    "HTML",
    "CSS",
    "C++",
    "C",
    "Lua",
    "Luau",
    "Java",
]
Languages = [
    "pt-BR",
    "en-US"
]
sg.theme("DarkAmber")
sg.DEFAULT_FONT = "Lexend"
sg.TOOLTIP_FONT = "Lexend"
sg.CUSTOM_TITLEBAR_FONT = "Lexend"
buttons = []
saidElement = sg.Text("You said: ", text_color="#fff", justification="left", font="Lexend 10 bold",)
responseElement = sg.Text("Response: ", text_color="#fff", size=(50, 1), justification="left", font="Lexend 10 bold",)

conversionCode = {
    "Python": "py",
    "JavaScript": "js",
    "HTML": "html",
    "CSS": "css",
    "C++": "cpp",
    "C": "c",
    "Lua": "lua",
    "Luau": "lua",
    "Java": "java",
}

class App:
    def __init__(self, props):
        for key, value in props.items():
            setattr(self, key, value)
        pass
    def Init(self):
        print(f"""
                [VRS] Initializing Speech Recognition App
                [VRS] Name: {getattr(self, 'name')}
                [VRS] Version: {getattr(self, 'version')}
               """, "cyan")
        # Init Voice Recognition

        self.CreateAppWindow()
        pass
    def CreateAppWindow(self):
        self.name = getattr(self, "name")
        self.version = getattr(self, "version")
        self.layout = getattr(self, "layout")
        self.marginSize = getattr(self, "marginSize")
        self.InputText = ""
        self.SETTINGS = getattr(self, "settings")
        window = sg.Window(
            title=f"{self.name} - {self.version}",
            layout=self.layout,
            margins=self.marginSize,
            icon="./assets/icon.ico"
            )
        while True:
            event, values = window.read() # type: ignore
            if event == sg.WIN_CLOSED or event == 'Exit':
                print("[VRS]: Window Closed!", "red")
                window.Close()
                break
            if event == "Save Settings":
                settings = {
                    "voice": values[2],
                    "language": values[1],
                    "codeLanguage": values[0],
                    "volume": values[3]
                }
                with open("./settings/main.json", "w") as file:
                    json.dump(settings, file)
                msg("Settings saved with success!", "[VRS] Notification")
            if event == "Record":
                print("[VRS]: Recording Voice", "green")
                text = main.record_text(values[1])
                self.InputText = text
                print(f"[VRS]: You said: {self.InputText}", "yellow")
                saidElement.Update(f"You said: {self.InputText}")
            if event == "Assistant":
                if self.InputText == "":
                    print("[VRS]: You need to say something and select a language.", "red")
                    continue

                ##for Command in CMDS:
                ##CommandName = Command["name"]
                #Similarity = STS.run(self.InputText, CommandName) # type: ignore
                ##if Similarity > 75:
                #print(f"Command: {CommandName} ({Similarity}%)", "cyan")

                RESPONSE = Commands.RunCommand(self.InputText, {   #type:ignore
                    "voice": values[2],
                    "language": values[1],
                    "codeLanguage": values[0],
                    "volume": values[3]
                })
                #print(f"[VRS]: {RESPONSE}", "yellow")
                
                HasCommandRun = RESPONSE
                    
                if HasCommandRun == False:
                    print("[VRS]: Sending Text to OpenAI's API", "green")
                    text = self.InputText
                    response = main.send_to_chatgpt([{"role": "user", "content": text}])
                    responseElement.Update(f"Response: {response}")
                    print(f"[ChatGPT]: {response}", "yellow")
                    if values[2] == True:
                        print('')
                        OpenAI.Speak(response) #type: ignore
                        #main.speak_text(response, values[1], values[3]/100)
                else:
                    pass

            if event == "Code":
                if self.InputText == "" or values[0] == None:
                    print("[VRS]: You need to say something and select a programming language.", "red")
                    continue

                print("[VRS]: Sending Text to OpenAI's API", "green")
                text = self.InputText
                language = values[0]
                parameters = open("./assets/parameters.txt", "r").read()
                initialParameters = f"{parameters}:\n{text} em {language}"
                print(str(text))
                code = OpenAI.Chat(messages=[{"role": "user", "content": initialParameters}], temperature=1)
                time = Date.now()
                fileDate = f"{time.day}_{time.month}_{time.year}-{time.hour}-{time.minute}-{time.second}"
                fileName = f"code_{fileDate}"
                extension = conversionCode[language]
                with open(f"./scripts/{fileName}.{extension}", 'w') as f:
                    f.write(str(code))
                    print(f"[VRS]: Code created: {fileName}.{extension}", "cyan")
                    codePath = System.path.abspath(f"./scripts/{fileName}.{extension}")
                    Shell(f'code "{codePath}"')
        pass

if __name__ == '__main__':
    SETTINGS = json.loads(open("./settings/main.json", "r").read())

    row1Buttons = [
        sg.Button("Record", size=btnSize, button_color="#03fc39", font="Lexend 10 bold", border_width=0),
        sg.Button("Exit", size=btnSize, button_color="#ff0000", font="Lexend 10 bold", border_width=0),
        sg.Button("Assistant", size=btnSize, button_color="#74AA9C", font="Lexend 10 bold", border_width=0),
    ]
    row2Buttons = [
        sg.Button("Code", size=btnSize, button_color="#fc9803", font="Lexend 10 bold", border_width=0),
        sg.Button("Save Settings", size=btnSize, button_color="#03fc9d", font="Lexend 10 bold", border_width=0)
    ]

    rows = [
        [sg.Text("Voice Recognition Service", text_color="#fff", font="Lexend 25 bold", justification="center")],
        [sg.Text("Developed by Caioband and SinceVoid", font="Lexend 20 bold", text_color="#fff", justification="center")],
        [sg.Text("", size=(10, 2))],
        [saidElement],
        [responseElement],
        [sg.Text("", size=(10, 2))],
        [row1Buttons],
        [row2Buttons],
        [sg.Text("", size=(10, 2))],
        [
            sg.OptionMenu(
                CodingLanguages,
                default_value=SETTINGS["codeLanguage"],
                background_color="#333",
                text_color="#ddd",
                auto_size_text = True
            ),
            sg.OptionMenu(
                Languages,
                default_value=SETTINGS["language"],
                background_color="#333",
                text_color="#ddd",
                auto_size_text = True
            ),
            sg.Checkbox("Voice", default=SETTINGS["voice"], font="Lexend 5 bold"),
        ],
        [sg.Text("Volume", font="Lexend 10 bold")],
        [sg.Slider(range=(0, 100), default_value=SETTINGS["volume"], orientation="h", size=(30,13), font = "Lexend 10 bold", border_width=0)]
    ]
    app = App({
        "name": "SpeechRecognitionApp",
        "version": "1.0.0",
        "description": "Speech Recognition App",
        "layout": rows,
        "marginSize": (65,65),
        "settings": SETTINGS
    })
    app.Init()