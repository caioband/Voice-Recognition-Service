from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator

model_name = 'bert-base-nli-mean-tokens'

class SentenceService:
    def __init__(self, model_name: str = model_name):
        self.model = SentenceTransformer(model_name)

    def convert_items_to_english(self, wordslist):
        translator = Translator()
        finalList = []
        for i in wordslist:
            finalList.append(translator.translate(i))
        return finalList


    def get_similarity(self, sentence1, sentence2):
        sentence_vecs = self.model.encode([sentence1, sentence2])

        result = cosine_similarity(
            [sentence_vecs[0]], # type: ignore
            sentence_vecs[1:], # type: ignore
        )

        result = result[0][0]
        result *= 100
        result = str(result)[:5]
        result = float(result)

        return result
    def run(self, sentence1: str, sentence2: str):
        NewWords = self.convert_items_to_english([sentence1, sentence2])
        TextList = []
        for i in NewWords:
            TextList.append(i.text)
        return self.get_similarity(TextList[0], TextList[1])