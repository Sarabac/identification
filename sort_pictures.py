#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import config
import template_sqlite
import os
import shutil


def trier(data):
    """
    Create the struccture of the shorted folder.
    data: list(camera, espece, picture name).
    """
    tree = {d[0]: {"Pictures": {
        "Roe deers": list(), "Humans": list(),
        "Other species": list(), "Nothing": list()
    }, "Video": list()} for d in data}
    print(tree)
    correspondance = {
        "rien": "Nothing",
        "chevreuil": "Roe deers",
        "humain": "Humans",
    }
    for d in data:
        t = tree[d[0]]["Pictures"][correspondance.get(d[1], "Other species")]
        t.append(d[2])
    return tree


def create_folder(root, name):
    path = os.path.join(root, name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def copy_file(path, name):
    path_source = os.path.join(config.photos, name)
    path_target = os.path.join(path, os.path.split(name)[-1])
    shutil.copy2(path_source, path_target)


def create_tree(data, root="", name="sorted"):
    path = create_folder(root, name)
    print(path, data)
    if type(data) is list:
        for d in data:
            copy_file(path, d)
    else:
        for k in data.keys():
            create_tree(data[k], path, k)


conn = sqlite3.connect(config.base, detect_types=config.detect_types)
cursor = conn.cursor()

result = cursor.execute(template_sqlite.espece_on_photo)
create_tree(trier(result.fetchall()))
