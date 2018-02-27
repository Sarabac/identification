#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 21:54:03 2018

@author: luxis
"""
from datetime import datetime
import itertools
import sqlite3
from PIL import Image
import os
import re

import especes
import config
import template_sqlite as ts


def init_base(cursor):
    """
    Cree les tables qui composent la base de donnee.
    """
    for instr in ts.creation.split(";"):
        cursor.execute(instr)


def init_photo(cursor):
    """
    Parcours le dossier des photos et retourne les instructions
    pour les incorporer dans la base de donnee
    """
    # ## selection des ficher se terminant par ".jpg" ou ".JPG"
    verification = re.compile("([^\s]+(\.(?i)(jpg))$)")
    noms = [nom for nom in os.listdir(config.photos)
            if verification.search(nom)]
    # ## extraction des informations importantes
    infos = list()
    for nom in noms:
        data = Image.open(os.path.join(config.photos, nom))._getexif()
        infos.append({
            'file': nom,
            'marque': data[271],
            'model': data[272],
            # la date est transformee en objet datetime
            'date': datetime.strptime(data[36867], '%Y:%m:%d %H:%M:%S')

        })
    # ## insertion des informations dans les requetes sqlite
    for data in infos:
        cursor.execute(ts.create_camera, {
                "marque": data['marque'], "model": data['model']})
        cursor.execute(ts.create_photo, data)


def init_especes(cursor):
    """
    Incorpore les especes, caracteres et modalites
    dans les tables correspondantes.
    """
    # on ne prend que les variables definies dans le module
    esp = [e for e in dir(especes) if e[1] != "_"]
    for e in esp:
        # le nom de la variable devient le nom d'espece
        cursor.execute(ts.create_espece, {"espece": e})
        id_esp = cursor.lastrowid
        dic_caract = getattr(especes, e)
        # on entre dans les caracteres de l'espece
        for c in dic_caract.keys():
            cursor.execute(ts.create_caractere, {"espece": id_esp, "nom": c})
            # on recupere l'identifiant du caractere insere
            id_caractere = cursor.lastrowid
            # on incere les modalites du caractere
            for m in dic_caract[c]:
                cursor.execute(
                    ts.create_modalite,
                    {"nom": str(m), "id_caractere": id_caractere}
                )


def recursive_serie(avant, cursor, num):
    """
    Cree la liste des correspondances id_photo / num de serie
    """
    print(avant)
    instruc = {
        "serie": [{"id": num, "camera": avant[1], "debut": avant[0]}],
        "photo": list()
        }
    while True:
        instruc["photo"].append({"serie": num, "id": avant[2]})
        instruc["serie"][0]["fin"] = avant[0]
        apres = cursor.fetchone()
        if apres is None:
            return instruc
        elif (apres[0]-avant[0] > config.interval_photo) or (avant[1] != apres[1]):
            nouvelles = recursive_serie(apres, cursor, num+1)
            instruc["serie"] += nouvelles["serie"]
            instruc["photo"] += nouvelles["photo"]
            return instruc
        else:
            avant = apres


def init_serie(cursor):
    """
    remplis la colonne serie de la table Photo
    """
    cursor.execute(ts.select_date_photo)
    instructions = recursive_serie(cursor.fetchone(), cursor, 1)
    print(instructions["serie"])
    cursor.executemany(ts.create_serie, instructions["serie"])
    cursor.executemany(ts.update_photo, instructions["photo"])


def affichage_series(cursor):
    cursor.execute(ts.select_serie)
    a_afficher = dict()
    series = [i for i in cursor.fetchall()]
    a_afficher["cameras"] = sorted(list(set([s[1] for s in series])))
    a_afficher["dates"] = sorted(list(set([str(s[2].date()) for s in series])))
    a_afficher["cellules"] = dict()
    for coord in itertools.product(a_afficher["dates"], a_afficher["cameras"]):
        a_afficher["cellules"][coord] = list()
        for s in series:
            if s[1] == coord[1] and str(s[2].date()) == coord[0]:
                a_afficher["cellules"][coord].append({
                    "id": s[0],
                    "debut": str(s[2].time()),
                    "fin": str(s[2].time())
                    })
    return a_afficher


def affichage_photos(cursor, id_serie):
    affichage = dict(photos=list())
    # on commence par l'id et le chemin vers chaque photo
    cursor.execute(ts.select_photo, {"id_serie": id_serie})

    for id, chem in cursor.fetchall():
        affichage["photos"].append((
            int(id),
            os.path.join(config.photos, chem.encode())
        ))
    print(affichage)
    return affichage


def unicode2str(iterable):
    result = list()
    for a in iterable:
        ligne = list()
        for b in a:
            if isinstance(b, type("a".decode())):
                c = b.encode()
            else:
                c = b
            ligne.append(c)
        result.append(ligne)
    return result


def get_espece(cursor):
    result = list()
    cursor.execute(ts.ajax_get_espece)
    for ligne in unicode2str(cursor.fetchall()):
        esp = [ligne[0], ligne[1]]
        car = [ligne[2], ligne[3]]
        mod = [ligne[4], ligne[5]]
        result.append([i for i in [esp, car, mod] if None not in i])

    return result

if __name__ == "__main__":
    conn = sqlite3.connect(config.base, detect_types=config.detect_types)
    cursor = conn.cursor()

    print(get_espece(cursor))

    conn.commit()
    conn.close()
