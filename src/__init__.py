"""
Tut budet opisanie biblioteki
"""

from dataclasses import dataclass, field

from ._bar import Progressbar
from ._base import SemanticAwareAnalyser, SemanticAwareRecommender
from .essemble import Graph

__all__ = [
    "SHOW_BAR",
    "MULTIPROCESSING",
    "JUPITER_SUPPORT",
    "IGNORE_MISSING",
    "WARN_RETRAIN",
    "UPDATE_GRAPH",
    "SemanticAwareAnalyser",
    "essemble",
    "education",
    "Progressbar",
    "Graph",
    "SemanticAwareRecommender",
]


from . import _flags


def _s():
    _flags._show_bar = True


def _m():
    _flags._multiprocessing = True


def _jn():
    _flags._jupiter_support = True


def _im():
    _flags._ignore_missing = True


def _wr():
    _flags._warn_retrain = True


def _ug():
    _flags._update_graph = True


_id_dict = {
    "SHOW_BAR": _s,
    "MULTIPROCESSING": _m,
    "JUPITER_SUPPORT": _jn,
    "IGNORE_MISSING": _im,
    "WARN_RETRAIN": _wr,
    "UPDATE_GRAPH": _ug,
}


def _flagmethods(name):
    global _id_dict
    _id_dict[name]()


@dataclass(frozen=True, kw_only=True)
class Flag:
    name: str = field(init=True, default_factory=str)
    val: bool = field(init=False, default=True, repr=False)

    def __call__(self):
        _flagmethods(self.name)


SHOW_BAR = S = Flag(name="SHOW_BAR")
JUPITER_SUPPORT = JN = Flag(name="JUPITER_SUPPORT")
MULTIPROCESSING = M = Flag(name="MULTIPROCESSING")
UPDATE_GRAPH = UG = Flag(name="UPDATE_GRAPH")
WARN_RETRAIN = WR = Flag(name="WARN_RETRAIN")
IGNORE_MISSING = IM = Flag(name="IGNORE_MISSING")
