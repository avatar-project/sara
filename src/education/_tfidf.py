# -*- coding: utf-8 -*-

import math
import re
from collections import defaultdict

import numpy as np

from .._bar import Progressbar

__all__ = ["find_top_words", "_key_controller", "one_article_find_top_words"]


def find_top_words(corpus, top_words=5):
    """
    Custom TF-IDF implementation based on numpy argsort.

    :param keys: corpus (more than one article requires)
    :type keys: list
    :param top_words: number of TF-IDF counted top words, default ``5``
    :type top_words: int, optional
    :return: list of top rated TF-IDF words in corpus
    :rtype: list
    """
    from .._flags import _show_bar

    if _show_bar:
        bar = Progressbar(prefix="TF calculation:  ", total=len(corpus))

    idf_dict = {}
    tf_dict = defaultdict(dict)
    for inx, doc in enumerate(corpus):
        added = []
        for word in doc:
            if word in tf_dict[inx].keys():
                tf_dict[inx][word] += 1
            else:
                tf_dict[inx][word] = 1
            if word not in idf_dict:
                idf_dict[word] = 1
            elif word not in added:
                idf_dict[word] += 1
            added.append(word)
        for k in tf_dict[inx].keys():
            tf_dict[inx][k] /= len(doc)
        if _show_bar:
            bar.update()

    if _show_bar:
        bar2 = Progressbar(
            prefix="IDF calculation: ",
            total=len(tf_dict.keys()),
        )

    for key, value in tf_dict.items():
        for word in value.keys():
            tf_dict[key][word] *= math.log((1 + len(corpus)) / (idf_dict[word] + 1)) + 1
        if _show_bar:
            bar2.update()

    if _show_bar:

        bar3 = Progressbar(
            prefix="Sorting:         ",
            total=len(tf_dict.keys()),
        )

    keys = []
    for _, val in tf_dict.items():
        # convs = dict.fromkeys([0, 1], bytes.decode)
        dtype = [("word", "U10"), ("tfifd", float)]
        values = list(val.items())
        _a = np.array(values, dtype=dtype)
        for _w in np.sort(_a, order="tfifd", kind="mergesort")[0:top_words]:
            word = re.sub(r"b'", "", str(_w[0]))
            word = re.sub(r"'", "", word)

            if word not in keys:
                keys.append(word)
        if _show_bar:
            bar3.update()

    return keys, idf_dict


def _func_chunk(lst, n):
    for x in range(0, len(lst), n):
        e_c = lst[x : n + x]

        if len(e_c) < n:
            e_c = e_c + [None for y in range(n - len(e_c))]
        yield e_c


def _key_controller(keys: list, keys_per_object: int = 500, number_of_keys: int = None):
    """
    A technical function that divides a set of keys into groups for analysis using multithreading.

    :param keys: list of keys
    :type keys: list
    :param keys_per_object: size of one iteration for muliprocessing, default ``500``
    :type keys_per_object: int, optional
    :param number_of_keys: optional parameter for slice the number of keys. Including can affect the efficiency of the model, default ``None``
    :type number_of_keys: int, optional
    :return: list of lists with splitted keys
    :rtype: list
    """

    if number_of_keys:
        keys = keys[:number_of_keys]

    new_keys = []
    for i, key1 in enumerate(keys):
        for j, key2 in enumerate(keys):
            if j > i:
                new_keys.append(f"{key1}_{key2}")

    final_keys = list(_func_chunk(new_keys, keys_per_object))

    final_keys[-1] = [x for x in final_keys[-1] if x]

    return final_keys


def one_article_find_top_words(
    _clear_article_without_sentences: list,
    idf_dict: dict,
    number_of_documents,
    top_words: int = 5,
    _added_already_flag=False,
):
    """
    A technical function that divides a set of keys into groups for analysis using multithreading.

    :param _clear_article_without_sentences: list of words
    :type keys: list
    :param idf_dict:
    :type idf_dict: dict
    :param top_words: number of TF-IDF counted top words, default ``5``
    :type top_words: int, optional
    :return: list of top rated TF-IDF words in corpus
    :rtype: list
    """
    tf_dict = {}
    _zeta = 1 / len(_clear_article_without_sentences)
    if not _added_already_flag:
        number_of_documents += 1
        added = []
        for word in _clear_article_without_sentences:
            try:
                tf_dict[word] += _zeta
            except:
                tf_dict[word] = _zeta
            if (word in idf_dict.keys()) and (word not in added):
                idf_dict[word] += 1
            else:
                idf_dict[word] = 1
            added.append(word)
    else:
        for word in _clear_article_without_sentences:
            try:
                tf_dict[word] += _zeta
            except:
                tf_dict[word] = _zeta

    for word in tf_dict.keys():
        tf_dict[word] *= math.log((1 + number_of_documents) / (idf_dict[word] + 1)) + 1

    keys = []
    dtype = [("word", "U10"), ("tfifd", float)]
    values = list(tf_dict.items())
    _a = np.array(values, dtype=dtype)
    for _w in np.sort(_a, order="tfifd", kind="mergesort")[0:top_words]:
        word = re.sub(r"b'", "", str(_w[0]))
        word = re.sub(r"'", "", word)
        keys.append(word)

    return keys
