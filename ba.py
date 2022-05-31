import json
from random import randint
from tkinter import *

import src
from src import SemanticAwareRecommender


def clicked():
    for item in keys_list:
        test_user_matrix[item] = randint(0, 10)
    _tum = dict(
        sorted(test_user_matrix.items(), key=lambda item: item[1], reverse=True)
    )
    temp_t = ""
    for inx, (key, val) in enumerate(_tum.items()):
        if inx < 15:
            temp_t += f"\n{key}: {val}"
    text3 = f"User: {temp_t}"
    lbl3.configure(text=text3)

    rez: dict = a.recommend(user=test_user_matrix, articles=articles, top_words=5)
    sorted_rez = dict(sorted(rez.items(), key=lambda item: item[1], reverse=True))
    text4 = "Top articles:\n\n"
    for inx, (key, val) in enumerate(sorted_rez.items()):
        article_name: str = titles[key]
        _ts = article_name.split()
        article_name = ""
        for index, word in enumerate(_ts):
            article_name += f"{word} "
            if index % 3 == 0 and index != 0:
                article_name += "\n"

        if inx < 5:
            text4 += f"ID: {key}, value: {val}\n Название:\n {article_name}\n\n"
        else:
            continue
    lbl4.configure(text=text4)


if __name__ == "__main__":
    src.SHOW_BAR(), src.MULTIPROCESSING(), src.IGNORE_MISSING()

    a = SemanticAwareRecommender()

    corpus = []
    with open(
        "Files/train.jsonl",
        "r",
        encoding="utf-8",
    ) as json_file:
        json_list = list(json_file)

    articles = {}
    titles = {}
    json_list = json_list[0:50]
    for json_str in json_list:
        result = json.loads(json_str)
        corpus.append(result["source"])
        articles[result["paper_id"]] = 0
        titles[result["paper_id"]] = result["title"]

    # # print(result["paper_id"])

    # corpus = corpus[0:60]
    split_corpus = []
    for inx, key in enumerate(articles.keys()):
        # for article in corpus:
        split_article = ""
        split_article = " ".join(corpus[inx])
        split_corpus.append(split_article)
        articles[key] = split_article

    a.simple_load(split_corpus)
    a.train(top_words=5, keys_per_object=500)
    # print(a.graph.vef["loss"])
    a.compute_graph()
    a.save()

    window = Tk()
    window.title("Демо SARS")
    window.geometry("700x800")

    text = f"Демо версия SARS.\n Текущее число статей: {len(corpus)}\n "
    lbl = Label(window, text=text, font=("Arial", 20))
    lbl.grid(column=0, row=0)

    test_user_matrix = {}
    keys_list = a.graph.nodes
    for item in keys_list:
        test_user_matrix[item] = 0

    btn = Button(window, text="Создать пользователя", command=clicked)
    btn.grid(column=0, row=1)

    # text2 = f"Список ключей: {keys_list}"
    # lbl2 = Label(window, text=text2, font=("Arial", 20))
    # lbl2.grid(column=0, row=1)

    temp_t = ""
    for key, val in test_user_matrix.items():
        temp_t += f"\n{key}: {val}"
    text3 = f"User: {temp_t}"
    lbl3 = Label(window, text=text3, font=("Arial", 20))
    lbl3.grid(column=0, row=2)

    text4 = ""
    lbl4 = Label(window, text=text4, font=("Arial", 20), anchor="n", justify=LEFT)
    lbl4.grid(column=1, row=2)

    scr_br = Scrollbar(window)
    window.mainloop()
