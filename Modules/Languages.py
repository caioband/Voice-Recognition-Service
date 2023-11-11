import googletrans as gt

class Translator:
    def __init__(self) -> None:
        self.Translator = gt.Translator()
        pass

    def Translate(self, settings, text: str) -> str:
        language = self.FormatToGoogle(settings["language"]) # [pt-BR, en-US, es-ES, ...]

        RESULT = self.Translator.translate(text,language)
        TEXT = RESULT.text  # type: ignore
        return str(TEXT)

    def FormatToGoogle(self, current: str):
       return current[:2].lower()