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
    dossiers = [nom for nom in os.listdir(config.photos)]
    # ## extraction des informations importantes
    infos = list()
    # changer pour "nom du fichier"
    for dossier in dossiers:
        noms = [nom for nom in os.listdir(os.path.join(config.photos, dossier))
                if verification.search(nom)]
        for nom in noms:
            img = Image.open(os.path.join(config.photos, dossier, nom))
            data = img._getexif()
            infos.append({
                'file': os.path.join(dossier, nom),
                'marque': data[271],
                'model': dossier,
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
                    "fin": str(s[3].time())
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
    return affichage


def definition_html(cursor):
    result = dict()

    cursor.execute("SELECT id_espece, nom_espece FROM Espece;")
    result["especes"] = list(cursor.fetchall())

    instr = """SELECT fk_espece, id_caractere, nom_caractere FROM Caractere;"""
    cursor.execute(instr)
    result["caracteres"] = dict()
    for fk, id, nom in cursor.fetchall():
        if fk not in result["caracteres"].keys():
            result["caracteres"][fk] = [(id, nom)]
        else:
            result["caracteres"][fk].append((id, nom))
    instr = """SELECT fk_caractere, id_modalite, nom_modalite FROM Modalite;"""
    cursor.execute(instr)
    result["modalites"] = dict()
    for fk, id, nom in cursor.fetchall():
        if fk not in result["modalites"].keys():
            result["modalites"][fk] = [(id, nom)]
        else:
            result["modalites"][fk].append((id, nom))
    return result


def enregistrer_animaux(cursor, animaux):
    """
    animaux: de la forme [{id_e: x, photos:[x,x,x], modalites:[x,x,x,x,x]}...]
    """
    # on commence par supprimer les precedents enregistrements
    #  qui ont eventuellement eu lieu sur les photos
    cursor.execute(ts.detruire_animal_sur_photo, {"id_serie": animaux["serie"]})

    for ind in animaux["individus"]:
        data = {"fk_espece": ind["id_e"], "date_entree": datetime.today()}
        cursor.execute(ts.create_animal, data)
        id_a = cursor.lastrowid
        for id_p in ind["photos"]:
            data = {"fk_photo": id_p, "fk_animal": id_a}
            cursor.execute(ts.pointer, data)
        for id_m in ind["modalites"]:
            data = {"fk_modalite": id_m, "fk_animal": id_a}
            cursor.execute(ts.caracteriser, data)


def charger(cursor, serie):
    cursor.execute(ts.extract_animal_serie, {"id_serie": serie})
    animaux = [i for i in cursor.fetchall()]
    result = list()
    print("aniamux:",animaux)
    for id in animaux:
        cursor.execute(
            "SELECT fk_photo FROM Pointer WHERE fk_animal=?", id
        )
        photos = [i[0] for i in cursor.fetchall()]
        cursor.execute(
            "SELECT fk_modalite FROM Caracteriser WHERE fk_animal=?", id
        )
        modalites = [i[0] for i in cursor.fetchall()]
        cursor.execute(
            "SELECT fk_espece FROM Animal WHERE id_animal=?", id
        )
        esp = cursor.fetchall()
        result.append({
            "id": esp[0],
            "photos": photos,
            "modalites": modalites
        })
    print(result)
    return result

if __name__ == "__main__":
    conn = sqlite3.connect(config.base, detect_types=config.detect_types)
    cursor = conn.cursor()


    print(charger(cursor, 1))

    conn.commit()
    conn.close()
