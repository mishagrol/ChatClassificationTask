import joblib
import os
import pickle
import numpy as np

# nlp
import re
import nltk
from nltk.corpus import stopwords
import string
import pymorphy2

import warnings

warnings.filterwarnings("ignore")


class ChatClassifier:
    def __init__(
        self,
        model_path: str,
        vectorizer_path: str,
    ) -> None:
        nltk.download("stopwords")
        self.model = joblib.load(model_path)
        self.vectorizer = pickle.load(open(vectorizer_path, "rb"))
        self.stopWords = set(stopwords.words("russian"))
        self.SYMBOLS = " ".join(string.punctuation).split(" ") + ["-", "...", "”", "”"]
        self.morph = pymorphy2.MorphAnalyzer()

    def str_preprocess(self, text: str) -> list:
        """
        Function to clean text and create lemmas
        """
        reg = re.compile("[^а-яА-яa-zA-Z0-9 ]")  #
        text = text.lower().replace("ё", "е")
        text = text.replace("ъ", "ь")
        text = text.replace("й", "и")
        text = text.replace("\\n", "")
        text = text.replace("\\r", "")
        text = text.replace("\\t", "")
        text = re.sub("((www\.[^\s]+)|(https?://[^\s]+))", "сайт", text)
        text = re.sub("@[^\s]+", "пользователь", text)
        text = reg.sub(" ", text)

        # Лемматизация
        text = " ".join([word for word in text.split() if word not in self.SYMBOLS])
        text = [
            self.morph.parse(word)[0].normal_form
            for word in text.split()
            if word not in self.stopWords
        ]
        return " ".join(text)

    def predict(self, text: str) -> dict:
        """
        Function to make prediction
        """
        text = self.str_preprocess(text)
        transormed_text = self.vectorizer.transform([text])
        predicted = self.model.predict(transormed_text)[0]
        probability = np.max(self.model.predict_proba(transormed_text)[0])
        return {"label": predicted, "probability": np.round(probability, 2)}


if __name__ == "__main__":
    classifier = ChatClassifier(
        model_path=os.path.join("..", "data", "logistic_reg_model.joblib"),
        vectorizer_path=os.path.join("..", "data", "vectorizer.pickle"),
    )
    result = classifier.predict(
        text="если у тебя нет верхнего предела, фиксед поинт это проблема"
    )
    print(result)
