import json
import os as System


class Application:
    def __init__(self) -> None:
        SETTINGS = {}
        if not (System.path.exists(r"../settings/main.json")):
            open(r"../settings/main.json", "w", encoding='utf-8').write('{"voice": true, "language": "pt-BR", "codeLanguage": "HTML", "volume": 100}')
        else:
            SETTINGS = json.loads(
                open(r"../settings/main.json", "r", encoding='utf-8').read())

        self.Settings = SETTINGS

    def Load_Settings(self) -> dict:
        return self.Settings

    def Write_Settings(self, newSettings: dict) -> dict:
        open(r"../settings/main.json", "w",
             encoding='utf-8').write(json.dumps(newSettings))
        self.Settings = newSettings
        return self.Settings

    def Update_Setting(self, key: str, value) -> dict:
        Settings = self.Load_Settings()
        Settings[key] = value
        self.Write_Settings(Settings)
        return Settings


App = Application()
