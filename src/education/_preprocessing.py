# -*- coding: utf-8 -*-

import re

import nltk
from pymorphy2 import MorphAnalyzer

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("punkt", quiet=True)

__all__ = ["text_filter"]

c_dict = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he's": "he is",
    "how'd": "how did",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'll": "i will",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'll": "it will",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "must've": "must have",
    "mustn't": "must not",
    "needn't": "need not",
    "oughtn't": "ought not",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "that'd": "that would",
    "that's": "that is",
    "there'd": "there had",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "where'd": "where did",
    "where's": "where is",
    "who'll": "who will",
    "who's": "who is",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "1st": "first",
    "2nd": "second",
    "3rd": "third",
    "4th": "forth",
    "5th": "fifth",
    "6th": "sixth",
    "7th": "seventh",
    "8th": "eighth",
    "9th": "ninth",
}


def text_filter(article: str, lang: str) -> list[str]:
    """
    Text filtration method. It is a deep text preprocessing generator based on `nltk <https://www.nltk.org/>`_ and `pymorphy2 <https://pymorphy2.readthedocs.io/en/stable/>`_  libs.

    :param path: article
    :type path: str
    """
    article = nltk.tokenize.sent_tokenize(article)
    if lang == "russian":
        lemmatizer = MorphAnalyzer()
    elif lang == "english":
        lemmatizer = nltk.stem.WordNetLemmatizer()
    stop_words = set(nltk.corpus.stopwords.words(lang))
    for sentence in article:
        text = re.sub("\n", " ", str(sentence))
        text = text.lower()
        if lang == "english":
            text = text.split()
            new_text = []
            for word in text:
                if word in c_dict:
                    new_text.append(c_dict[word])
                else:
                    new_text.append(word)
            text = " ".join(new_text)
        text = re.sub(r"<.*?>", " ", text)
        text = re.sub(r"https?:\/\/.*[\r\n]*", " ", text, flags=re.MULTILINE)
        text = re.sub(r"\<a href", " ", text)
        text = re.sub(r"&amp;", " ", text)
        text = re.sub(r"<br />", " ", text)
        text = re.sub(r"\'", " ", text)
        text = re.sub(r">", " ", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub("[^a-z]+ ", "", text)
        while "  " in text:
            text = text.replace("  ", " ")
        text = text.split()
        text = [w for w in text if not w in stop_words]
        if lang == "russian":
            l_text = [lemmatizer.parse(token)[0].normal_form for token in text]
        elif lang == "english":
            l_text = [lemmatizer.lemmatize(token) for token in text]
        yield l_text
