# -*- coding: utf-8 -*-
import os
import sys
import warnings

import gensim
import numpy as np

__all__ = ["w2v_edu", "w2v_analys", "w2v_add"]


def _gen_cycle(article: list, min_count: int, tick: int):
    """
    Recursive Word2Vec analysis model, with starting value `min_count`

    :param article: article splited by sentences
    :type article: list[lists]
    :param min_count: Start value `gensim.models.Word2Vec(min_count) <https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#min-count>`_. Each failed iteration decrease value by one.
    :type min_count: int
    :param tick: not set by the user. need for saving
    """
    try:
        model = gensim.models.Word2Vec(
            sentences=article, vector_size=300, window=10, min_count=5, workers=1
        )
        model.save(f"{os.getcwd()}/__pycache__/w2v/m_{tick}.model")
    except:
        _gen_cycle(article, min_count - 1, tick)


def w2v_edu(corpus: list, min_count: int = 10):
    """
    Main educational method. It creates gensim Word2Vec models and cache them into `__pycache__` forlder in current working directory. For each text file creates own model.

    :param article: preprocessed corpus split by texts and senteces.
    :type article: list[lists]
    :param min_count: Start value `gensim.models.Word2Vec(min_count) <https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#min-count>`_. Each failed iteration decrease value by one throught `_gen_cycle`.
    :type min_count: int
    """
    tick = 0
    for article in corpus:
        try:
            model = gensim.models.Word2Vec(
                sentences=article,
                vector_size=300,
                window=10,
                min_count=min_count,
                workers=1,
            )
            model.save(f"{os.getcwd()}/__pycache__/w2v/m_{tick}.model")
            tick += 1
        except:
            try:
                _gen_cycle(article, min_count - 1, tick)
                tick += 1
            except:
                continue


def w2v_analys(words: str):
    """
    Inverse function for parsing prepared keywords. Extracts from buffer of the w2v model and makes a comparative analysis with the search for the largest value.

    :param words: two splited keywords in form of ``f'{word1}_{word2}'``
    :type words: str
    """
    words = words.split("_")
    _word_1 = words[0]
    _word_2 = words[1]
    values = []
    size = _amount()
    for i in range(size):
        model = gensim.models.Word2Vec.load(
            f"{os.getcwd()}/__pycache__/w2v/m_{i}.model"
        )
        try:
            sims = model.wv.similarity(_word_1, _word_2)  # get similarity
            values.append(sims)
        except:
            0

    if len(values) != 0:
        value = np.mean(values)
    else:
        value = 0
    return value


def _amount():
    size = 0
    for _, _, files in os.walk(f"{os.getcwd()}/__pycache__/w2v/"):
        for _ in files:
            size += 1
    return size


def w2v_add(article: list, min_count: int = 10):
    """
    Function to add a one separate model.

    :param article: Article in form of list split by sentences
    :type article: list[str]
    :param min_count: Start value `gensim.models.Word2Vec(min_count) <https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#min-count>`_. Each failed iteration decrease value by one.
    :type min_count: int
    """
    try:
        model = gensim.models.Word2Vec(
            sentences=article, vector_size=100, window=5, min_count=min_count, workers=1
        )
        model.save(f"{os.getcwd()}/__pycache__/w2v/m_{_amount()}.model")
    except:
        try:
            _gen_cycle(article, min_count - 1, _amount() + 1)
        except:
            warnings.warn("\nModel couldn't be saved. Check the format of article\n\n")
            sys.exit(1)
