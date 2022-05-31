# -*- coding: utf-8 -*-
import multiprocessing
import os
import pickle
import shutil
from dataclasses import dataclass, field
from itertools import repeat

from ._bar import Progressbar
from .education import (
    Loader,
    _encounter,
    _key_controller,
    article_load,
    find_top_words,
    one_article_find_top_words,
    w2v_edu,
)
from .essemble import Graph, _ad_c, count_weight_recommender

__all__ = ["SemanticAwareAnalyser", "SemanticAwareRecommender", "_sars_base"]


@dataclass
class _sars_base(Loader):
    """
    This class is technical part for cross-inheriting and shouldn't be called itself.

    .. tip::
        You can read more about specific methods and functions in :ref:`TRAINING MODULE`

    """

    keys: list = field(default_factory=list, init=False, repr=False)
    multikeys: list = field(default_factory=list, init=False, repr=False)
    graph: Graph = field(default_factory=Graph, init=False, repr=False)
    _idf_dict: dict = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        pathes = [
            "src/__pycache__",
            "src/education/__pycache__",
            "src/essemble/__pycache__",
        ]
        for path in pathes:
            try:
                shutil.rmtree(path)
            except:
                continue
        super().__init__()
        # self._load_preprocessed()

    def train(
        self, top_words: int = 5, keys_per_object: int = 500, number_of_keys: int = None
    ):
        """
        Main training method universal for :ref:`SemanticAwareAnalyser<SemanticAwareAnalyser>` and :ref:`SemanticAwareRecommender<SemanticAwareRecommender>`. Uses the corpus to train Word2Vec models and create simple paths for the graph.

        :param top_words: the number of words that will be extracted from each text by the TF-IDF method, defaults to 5
        :type top_words: int, optional
        :param keys_per_object: the number of word links in one Epoch of model training, defaults to 500
        :type keys_per_object: int, optional
        :param number_of_keys: optional ability to limit the number of keys. Cuts off the least popular ones, defaults to None
        :type number_of_keys: int, optional

        .. note::
            Default value for ``keys_per_object`` (in one Epoch) if 500, based on 200 text files in corpus. If you want to change it you can count optimal value by yourself using this simple formulae:

            .. math::
                :label: keys_per_object_count

                N = frac_{n*(n-1)/2}{i*3}

            where ``n`` is the number of keywords and ``i`` is the number of cores in your CPU.
        """
        from ._flags import _multiprocessing, _show_bar

        w2v_edu(self._clear_corpus_split_by_sentence)
        self.keys, self._idf_dict = find_top_words(
            self._clear_corpus_without_sentences, top_words=top_words
        )
        self.multikeys = _key_controller(
            self.keys, keys_per_object=keys_per_object, number_of_keys=number_of_keys
        )

        if _multiprocessing:
            if _show_bar:
                print(
                    "\n\n\t       WARNING!\n  To prevent unreadable output in Terminal progress bar isn't shown during multiprocessing calculations.\n"
                )
            pool = multiprocessing.Pool(multiprocessing.cpu_count())
            node_list = pool.starmap(
                _encounter,
                zip([keys for keys in self.multikeys], repeat(_multiprocessing)),
            )
        else:
            if _show_bar:
                bar = Progressbar(
                    prefix="Education:       ",
                    total=len(self.multikeys),
                )
            node_list = []
            for keys in self.multikeys:
                node_list.append(_encounter(keys, _multiprocessing))
                if _show_bar:
                    bar.update()

        for nodes in node_list:
            self.graph.add_nodes(nodes=nodes)
        self.graph._integrity_check()

    def compute_graph(self, calculus_type="minus"):
        """
        Method for bringing a graph to a connected form. The use of this function during training saves time in the further use of the model at times. For more information look the :ref:`calculus types<Calculus types>`.

        :param calculus_type: The method of graph cross-search, default= ``'minus'`` :eq:`minus_calc`
        :type calculus_type: str, optional
        """
        from ._flags import _show_bar

        gen = _ad_c(self.graph, calculus_type=calculus_type)

        if _show_bar:
            bar = Progressbar(
                prefix="Graph transform: ",
                total=(len(self.graph.vef.keys()) ** 2 - len(self.graph.vef.keys()))
                // 2,
            )

        for string, element, path_len in gen:
            self.graph.vef[string][element] = path_len
            if _show_bar:
                bar.update()
        print("graph vse")
        for key, _ in self.graph.vef.items():
            self.graph.vef[key][key] = 1

        self.graph._integrity_check()

    def save(self, path: str = f"{os.getcwd()}/model.saa"):
        """
        Method to save the model based on ``pickle`` library

        :param path: path to the location where to save, defaults to f"{os.getcwd()}/model.saa"
        :type path: str, optional
        """
        with open(path, "wb") as handle:
            pickle.dump(self, handle)

    def load(self, path: str = f"{os.getcwd()}/model.saa"):
        """
        Method to load the pretrained model based on ``pickle`` library

        :param path: path to the location where from to load, defaults to f"{os.getcwd()}/model.saa"
        :type path: str, optional
        """
        with open(path, "rb") as fp:
            self = pickle.load(fp)

    def __del__(self):
        pass


@dataclass(frozen=False)
class SemanticAwareAnalyser(_sars_base):
    """
    IN PROGRESS

    .. seealso::
        This class inherites the :ref:`Base class<Base class>`
    """

    def __post_init__(self):
        super().__post_init__()

    def analyse(self, articles: dict, top_words: int = 5):
        """
        IN PROGRESS

        :param articles: IN PROGRESS
        :type articles: dict
        :param top_words: IN PROGRESS, defaults to 5
        :type top_words: int, optional
        :return: IN PROGRESS
        :rtype: dict
        """
        # articles = {id: article}
        weights = {}
        for ID, article in articles.items():
            _clear_article_without_sentences, _ = article_load(
                article=article, lang=self.lang
            )
            _article_keys = one_article_find_top_words(
                _clear_article_without_sentences,
                idf_dict=self._idf_dict,
                number_of_documents=1,
                top_words=top_words,
            )
            weights[ID] = count_weight_recommender(self.graph, _article_keys, None)
        return weights


@dataclass(frozen=False)
class SemanticAwareRecommender(_sars_base):
    """
    IN PROGRESS

    .. seealso::
        This class inherites the :ref:`Base class<Base class>`
    """

    def __post_init__(self):
        super().__post_init__()

    def recommend(self, user: dict, articles: dict, top_words: int = 5):
        """
        IN PROGRESS

        :param user: IN PROGRESS
        :type user: dict
        :param articles: IN PROGRESS
        :type articles: dict
        :param top_words: IN PROGRESS, defaults to 5
        :type top_words: int, optional
        :return: IN PROGRESS
        :rtype: dict
        """
        from ._flags import _multiprocessing

        # articles = {id: article}
        weights = {}
        n_d = len(self.corpus)
        _all_keys = []
        for ID, article in articles.items():
            if article in self.corpus:
                _added_already_flag = True
            _clear_article_without_sentences, _ = article_load(
                article=article, lang=self.lang
            )
            _all_keys.append(
                one_article_find_top_words(
                    _clear_article_without_sentences,
                    idf_dict=self._idf_dict,
                    top_words=top_words,
                    number_of_documents=n_d,
                    _added_already_flag=_added_already_flag,
                )
            )

        if _multiprocessing:
            pool = multiprocessing.Pool(multiprocessing.cpu_count())
            _ws = pool.starmap(
                count_weight_recommender,
                zip(repeat(self.graph), [keys for keys in _all_keys], repeat(user)),
            )
            for inx, ID in enumerate(articles.keys()):
                weights[ID] = _ws[inx]
                pass
        else:
            for inx, ID in enumerate(articles.keys()):
                weights[ID] = count_weight_recommender(self.graph, _all_keys[inx], user)
        return weights
