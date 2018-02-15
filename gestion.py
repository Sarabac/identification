#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 21:54:03 2018

@author: luxis
"""
from datetime import datetime
import config
import template_sqlite as ts
import sqlite3
from PIL import Image
import os
import re
import especes


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
    noms = [nom for nom in os.listdir(config.photos) if verification.search(nom)]
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
        cursor.execute(ts.create_camera, {"marque": data['marque'], "model": data['model']})
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
        dic_caract = getattr(especes, e)
        # on entre dans les caracteres de l'espece
        for c in dic_caract.keys():
            cursor.execute(ts.create_caractere, {"espece": e, "nom": c})
            # on recupere l'identifiant du caractere insere
            id_caractere = cursor.lastrowid
            # on incere les modalites du caractere
            for m in dic_caract[c]:
                cursor.execute(ts.create_modalite,
                    {"nom": str(m), "id_caractere": id_caractere})


def recursive_serie(avant, cursor, num):
    """
    Cree la liste des correspondances id_photo / num de serie
    """
    instruc = list()
    while True:
        instruc.append({"serie": num, "id": avant[2]})
        apres = cursor.fetchone()
        if apres is None:
            return instruc
        elif (apres[0]-avant[0] > config.interval_photo) or (avant[1] != apres[1]):
            return instruc + recursive_serie(apres, cursor, num+1)
        else:
            avant = apres


def init_serie(cursor):
    """
    remplis la colonne serie de la table Photo
    """
    cursor.execute(ts.select_date_photo)
    instructions = recursive_serie(cursor.fetchone(), cursor, 1)
    cursor.executemany(ts.create_serie, instructions)

if __name__ == "__main__":
    conn = sqlite3.connect(config.base, detect_types = config.detect_types)
    cursor = conn.cursor()

    conn.commit()
    conn.close()
