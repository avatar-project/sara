# -*- coding: utf-8 -*-

from .._bar import Progressbar
from ._preprocessing import text_filter

__all__ = ["corpus_load", "article_load"]


def corpus_load(corpus: list[str], lang="english") -> list[list]:
    """
    The main method for loading the texts corpus into the :class:`SemanticAwareAnalyser` class.

    :param corpus: Corpus of articles
    :type corpus: list
    :param lang: articles language, supported langs are ``'english'`` and ``'russian'``, defaults to "english"
    :type lang: str, optional
    :return: returns preprocessed corpus in two different types for TF-IDF analys and Graph search
    :rtype: tuple
    """
    from .._flags import _show_bar

    _clear_corpus_without_sentences = []
    _clear_corpus_split_by_sentence = []

    if _show_bar:
        bar = Progressbar(prefix="Text filtering:  ", total=len(corpus))

    for article in corpus:

        if len(article) < 1:
            continue

        (
            _clear_article_without_sentences,
            _clear_article_split_by_sentence,
        ) = article_load(article, lang)
        _clear_corpus_without_sentences.append(_clear_article_without_sentences)
        _clear_corpus_split_by_sentence.append(_clear_article_split_by_sentence)

        if _show_bar:
            bar.update()

    return _clear_corpus_without_sentences, _clear_corpus_split_by_sentence


def article_load(article: str, lang: str):
    """
    Completed splitter for separate article to load it into ``_text_filter`` function

    :param article: article in form of python string or lstring
    :type article: str
    :param lang: articles language, supported langs are ``'english'`` and ``'russian'``, defaults to "english"
    :type lang: str
    :return: returns preprocessed separate article in two different types for TF-IDF analys and Graph search
    :rtype: tuple
    """

    _clear_article_without_sentences = []
    _clear_article_split_by_sentence = []
    for sent in text_filter(article, lang=lang):
        _clear_article_without_sentences += sent
        _clear_article_split_by_sentence.append(sent)

    return _clear_article_without_sentences, _clear_article_split_by_sentence
