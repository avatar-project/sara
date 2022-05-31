# -*- coding: utf-8 -*-
import logging
import os
import pickle
from collections import defaultdict
from dataclasses import dataclass, field

__all__ = ["Graph"]


@dataclass(frozen=False, slots=True)
class Graph:
    """
    Custom graph representation method.

    :param vef: dict with all nodes and paths between them. Initialized automatically with :func:`add_nodes` function
    :type vef: defaultdict(dict)
    :param nodes: list of all nodes. Initialized automatically with :func:`add_nodes` function
    :type nodes: list
    """

    vef: defaultdict = field(default_factory=defaultdict, init=False, repr=False)
    nodes: list = field(default_factory=list, init=False, repr=True)

    def add_nodes(self, nodes: defaultdict(dict)):
        """
        Simple nodes adding method

        :param nodes: dict of nodes to add
        :type nodes: defaultdict(dict)
        """
        for k in nodes:
            if k not in self.vef:
                self.vef[k] = {}
            for i, val in nodes[k].items():
                if i not in self.vef:
                    self.vef[i] = {}
                self.vef[i][k] = val
                self.vef[k][i] = val

        self._nodes_list()

    def delete_nodes(self, nodes_list: list):
        """
        Simple method to delete nodes

        :param nodes_list: list of nodes to delete
        :type nodes_list: list
        """
        for node in nodes_list:
            del self.vef[node]
            for k in self.vef:
                del self.vef[k][node]

    def save(self, name: str = "graph", path: str = os.path.dirname(__file__)):
        """
        Method to save graph separately of the model.

        :param name: Sets the name of the file where the graph will be saved, Default is ``"graph"``
        :type name: str, optional
        :param path: Specifies the folder where the file with the graph will be saved, By default - in the same folder as the file itself
        :type path: str, optional
        """
        with open(f"{path}/{name}.sag", "wb") as handle:
            pickle.dump(self.vef, handle)

    def load(self, name: str = "graph", path: str = os.path.dirname(__file__)):
        """
        Method to load graph to the model separately

        :param name: Sets the name of the file where the graph will be loaded from, Default - ``"graph"``
        :type name: str, optional
        :param path: Specifies the folder where the file with the graph will be loaded from, By default - in the same folder as the file itself
        :type path: str, optional
        """
        with open(f"{path}/{name}.sag", "rb") as fp:
            self.vef = pickle.load(fp)

    def _nodes_list(self):
        for key, _ in self.vef.items():
            if key not in self.nodes:
                self.nodes.append(key)
            for key2 in _:
                if key2 not in self.nodes:
                    self.nodes.append(key2)

    def _integrity_check(self):
        print("\n\n\t     --------INTEGRITY CHECK--------")
        _error_list = 0
        _error_fact = 1
        for node in self.nodes:
            for target in self.nodes:
                if target != node:
                    try:
                        self.vef[node][target]
                    except:
                        try:
                            self.vef[node][target] = self.vef[target][node]
                        except:
                            _error_fact = 0
                            _error_list += 1

        try:
            _error_fact / _error_fact
            print("\t     ---INTEGRITY CHECK COMPLETED---\n")
        except ZeroDivisionError:
            logging.exception(
                f"\n\t    ERROR!\n    The integrity of the graph is broken.\n    Full paths were not built in {_error_list} situations.\n\n"
            )
