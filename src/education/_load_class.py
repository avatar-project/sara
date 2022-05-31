# -*- coding: utf-8 -*-
import json
import os
from dataclasses import dataclass, field

from ._corpus_cleaner import article_load, corpus_load

__all__ = ["Loader"]


@dataclass(frozen=False)
class Loader:
    """
    ``Loader`` is an inherited class used in the learning method to load a corpus of articles into the system.
    """

    lang: str = field(default="english")
    corpus_path: str = field(default=f"{os.path.dirname(__file__)}/corpus.txt")
    corpus: list = field(default_factory=list, init=False, repr=False)
    _clear_corpus_without_sentences: list = field(
        default_factory=list, init=False, repr=False
    )
    _clear_corpus_split_by_sentence: list = field(
        default_factory=list, init=False, repr=False
    )

    def _load(self):
        (
            self._clear_corpus_without_sentences,
            self._clear_corpus_split_by_sentence,
        ) = corpus_load(corpus=self.corpus, lang=self.lang)

    def simple_load(self, corpus: list[str]):
        """
        A method for simply loading a corpus as a ``[list]`` of ``"strings"`` with texts.

        :param corpus: corpus
        :type corpus: list[str]
        """
        self.corpus = corpus
        self._load()

    def load_txt(self, path: str):
        """
        corpus txt loader function.

        :param path: path to the txt file (we recommend not to use absolutepaths)
        :type path: str
        """

        self.corpus_path = path
        with open(self.corpus_path, "r", encoding="utf-8") as file:
            for line in file:
                self.corpus.append(line.strip())

        self._load()

    def load_csv(self, path: str, column_name: str = "text", separator: str = ";"):
        """
        Corpus csv loader function.

        :param path: path to the csv file (we recommend not to use absolutepaths)
        :type path: str
        :param column_name: The name of the column to search by, by default "text"
        :type column_name: str, optional
        :param separator: separater, default ";"
        :type separator: str, optional
        """

        # требует отдельной зависимости
        import pandas

        self.corpus_path = path

        _df = pandas.read_csv(path, sep=separator)
        self.corpus = _df[column_name].values.tolist()

        self._load()

    def load_json(self, path: str, keyword: str = "content"):
        """
        Corpus json loader function.

        :param path: path to the json file (we recommend not to use absolutepaths)
        :type path: str
        :param keyword: The name of the keyword to search by, by default "content"
        :type keyword: str, optional
        """

        self.corpus_path = path
        with open(path, "r", encoding="utf-8") as json_file:
            json_list = list(json_file)

        for json_str in json_list:
            result = json.loads(json_str)
            self.corpus.append(result[keyword])

        self._load()

    def _load_sql(self, path: str):
        """
        STILL WORKING
        """
        pass

    def add_article(self, article: str):
        """
        Function to add separate article. Automatically adds a new article to all dependencies.

        :param article: text in form of string
        :type article: str
        """

        self.corpus.append(article)
        _temp_a, _temp_b = article_load(article=article, lang=self.lang)
        self._clear_corpus_without_sentences.append(_temp_a)
        self._clear_corpus_split_by_sentence.append(_temp_b)
