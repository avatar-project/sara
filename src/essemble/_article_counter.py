# -*- coding: utf-8 -*-
import logging
import sys
import warnings
from collections import defaultdict

from ..education import w2v_analys
from ._graph_class import Graph

__all__ = ["count_weight_recommender"]


def count_weight_recommender(graph: Graph, article: list, user_matrix: dict):
    """
    The function for ranking texts by semantic relationship for a specific user.

    :param graph: Preanalysed graph
    :type graph: Graph
    :param article: Dict of articles in form of string
    :type article: dict{ID: str}
    :param user_matrix: user matrix
    :type user_matrix: dict
    :return: weight of the article for the user
    :rtype: if UPDATE_GRAPH and WARN_RETRAIN -> tuple. else -> float
    """
    keys = graph.nodes
    from .._flags import _ignore_missing, _update_graph, _warn_retrain

    if _update_graph and not _warn_retrain:
        warnings.warn(
            "\n\nWARNING!\n   UPDATE_GRAPH flag is not supported without WARN_RETRAIN.\n     Combine both flags to inplement result.\n"
        )
    if _ignore_missing and _warn_retrain:
        warnings.warn(
            "\n\nEXCEPTION!\n   SYS.ERROR: IM and WR flags couldn't be used together\n"
        )
        sys.exit(1)

    if _ignore_missing:
        decrease_val = 0

    test_article = {}
    for key in article:

        if _warn_retrain:
            _retrain_ = []
            if _update_graph:
                _new_nodes = defaultdict(dict)

        rez = 0

        for element in article:

            if _ignore_missing:
                try:
                    rez += graph.vef[key][element] * user_matrix[element]
                except Exception:
                    decrease_val += 1
                if element == article[-1] and decrease_val > 0:
                    warnings.warn(
                        f"\n\nWARNING!\n   The use of the IGNORE_MISSING flag resulted in {decrease_val} words missing,\n     reducing the overall theoretical accuracy of the model by {round(decrease_val/(len(keys)*len(article))*100, 3)}%.\n"
                    )

            elif _warn_retrain:
                try:
                    rez += graph.vef[element][key] * user_matrix[element]
                except:
                    _tr = w2v_analys(f"{element}_{key}")
                    _retrain_.append(_tr)
                    if _update_graph and _tr != 0:
                        _new_nodes[key][element] = {"weight": _tr}
                    rez += _tr

            else:
                try:
                    rez += graph.vef[element][key] * user_matrix[element]
                except BaseException:
                    logging.exception(
                        "\n\nThe key: '%s' is not defined in graph. Use `IGNORE_MISSING` flag to elide KeyError. \nWe attend that using flags can insanly reduce the accuracy of the model.\n\n",
                        key,
                    )
                    sys.exit(1)

        if _warn_retrain and _update_graph:
            graph.add_nodes(nodes=_new_nodes)

        if _warn_retrain and (len(_retrain_) > 0) and (sum(_retrain_) < 1):
            warnings.warn(
                "\n\nWARNING!\n   Retraining was not effective.\n     Add another corpus models to complete the clear result\n"
            )
            if _update_graph:
                warnings.warn("\n\nWARNING!\n   No new nodes was added.\n")

        test_article[key] = rez

    if _update_graph and _warn_retrain:
        return sum(test_article.values()), graph
    else:
        return sum(test_article.values())
