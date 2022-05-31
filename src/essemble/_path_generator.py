# -*- coding: utf-8 -*-
import sys
import warnings

from ._graph_class import Graph

__all__ = ["return_all_paths", "search_path", "_ad_c"]


def _generate_simple_paths(
    vef: dict, source: str, target: str, visited: dict, path: list, _max_len: int = 3
):

    visited[source] = True
    path.append(source)

    if source == target:
        yield path
    else:
        if len(path) <= _max_len:
            for child in vef[source].keys():
                if visited[child] is False:
                    for paths in _generate_simple_paths(
                        vef, child, target, visited, path
                    ):
                        yield paths

    path.pop()
    visited[source] = False


def return_all_paths(graph: Graph, source: str, target: str, _max_len: int = 3):
    """
    Recursive breadth traversal generator. ``_max_len`` parameter is the depth of the passage through the graph.

    :param graph: Preanalysed graph
    :type graph: Graph
    :param source: Starting node
    :type source: str
    :param target: The goal node
    :type target: str
    :yield: path in form of ``[list]``
    :rtype: Generator
    """
    visited = {}
    for i in graph.nodes:

        visited[i] = False

    path = []
    for paths in _generate_simple_paths(
        graph.vef, source, target, visited, path, _max_len
    ):
        yield paths


def _minus_search(graph: Graph, source: str, target: str, _max_len: int = 3):

    path_length = []
    for path in return_all_paths(
        graph, source=source, target=target, _max_len=_max_len
    ):
        rez = 0
        for inx, element in enumerate(path):
            if inx == 1:
                rez = graph.vef[element][path[0]]
            elif inx > 1:
                rez -= graph.vef[element][path[inx - 1]] / (inx**2)
        path_length.append(rez)

    if len(path_length) != 0:
        return max(path_length)
    else:
        warnings.warn(
            f"\n\n    No path was found between nodes {source} and {target}\n Please, increase the `_max_len` value.\n"
        )
        sys.exit(1)


def _mean_search(graph: Graph, source: str, target: str, _max_len: int = 3):
    path_length = []
    for path in return_all_paths(
        graph, source=source, target=target, _max_len=_max_len
    ):
        rez = 0
        for inx, element in enumerate(path):
            if inx == 1:
                rez = graph.vef[element][path[0]]
            elif inx > 1:
                rez += graph.vef[element][path[inx - 1]]

        rez = rez / (inx + 1)
        path_length.append(rez)

    if len(path_length) != 0:
        return max(path_length)
    else:
        warnings.warn(
            f"\n\n    No path was found between nodes {source} and {target}\n Please, increase the `_max_len` value.\n"
        )
        sys.exit(1)


def _plus_search(graph: Graph, source: str, target: str, _max_len: int = 3):
    path_length = []
    for path in return_all_paths(
        graph, source=source, target=target, _max_len=_max_len
    ):
        rez = 0
        for inx, element in enumerate(path):
            if inx == 1:
                rez = graph.vef[element][path[0]]
            elif inx > 1:
                rez += graph.vef[element][path[inx - 1]] / (inx**2)
        path_length.append(rez)

    if len(path_length) != 0:
        return max(path_length)
    else:
        warnings.warn(
            f"\n\n    No path was found between nodes {source} and {target}\n Please, increase the `_max_len` value.\n"
        )
        sys.exit(1)


def _shortest(graph: Graph, source: str, target: str, _max_len: int = 3):
    pass


def _optimum_search(graph: Graph, source: str, target: str, _max_len: int = 3):
    pass


def search_path(
    calculus_type: str, graph: Graph, source: str, target: str, _max_len: int = 3
):
    """
    The technical function of splitting and invoking different types of path computation in a graph.

    :param calculus_type: The method of graph cross-search.
    :type calculus_type: str, default= ``'minus'`` :eq:`minus_calc`
    :param graph: Preanalysed graph
    :type graph: Graph
    :param source: Starting point
    :type source: str
    :param target: The goal node
    :type target: str
    :return: The best path value depens on ``calculus_type``
    :rtype: int or None
    """
    if calculus_type == "minus":
        return _minus_search(graph, source, target, _max_len)
    elif calculus_type == "mean":
        return _mean_search(graph, source, target, _max_len)
    elif calculus_type == "plus":
        return _plus_search(graph, source, target, _max_len)
    elif calculus_type == "shortest":
        return _shortest(graph, source, target, _max_len)
    elif calculus_type == "optimum":
        return _optimum_search(graph, source, target, _max_len)


def _ad_c(graph: Graph, calculus_type: str = "minus", _max_len: int = 3):

    keys = graph.nodes

    for inx1, source in enumerate(keys):
        for inx2, target in enumerate(keys):
            if inx2 > inx1:
                path_len = search_path(calculus_type, graph, source, target, _max_len)
                if path_len is not None:
                    yield source, target, path_len
