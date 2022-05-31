# -*- coding: utf-8 -*-
from collections import defaultdict

from ._word2vec import w2v_analys

__all__ = ["_encounter"]


def _encounter(words: list[str], _mp: bool = False):

    """
    Technical function for passing the list of keys to the analysis module Word2Vec and graph update.

    :param words: list of combined words in form of string
    :type words: list
    :return: updated nodelist for graph analys
    :rtype: defaultdict[dict]
    """

    nodes = defaultdict(dict)
    for pool in words:
        _s = pool.split("_")
        nodes[_s[0]][_s[1]] = w2v_analys(pool)

    if _mp:
        print(f"{words[0]}-{words[-1]} matrix completed")

    return nodes
