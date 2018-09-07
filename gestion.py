#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 21:54:03 2018

@author: luxis
"""
from datetime import datetime
import itertools
import sqlite3
# package pillow
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
    # les instruction sont executees les unes apres les autre
    # dans une liste.
    for instr in ts.creation.split(";"):
        cursor.execute(instr)


def create_photo(cursor, dossier):
    """
    Insert les photos du dossier dans la base de donnee et cree la camera
    correspondante si elle n'existe pas.
    """
    # si le dossier existe deja dans la base de donnee

    cursor.execute(
        "SELECT id_camera FROM Camera WHERE model=:dossier",
        {"dossier": dossier}
    )
    try:
        id_camera = cursor.fetchone()[0]
    # sinon on cree la camera correspondante
    except TypeError:
        cam = {
            'marque': "Camera",
            'model': dossier,
        }
        cursor.execute(ts.create_camera, cam)
        id_camera = cursor.lastrowid

    verification = re.compile("([^\s]+(\.(?i)(jpg))$)")
    cursor.execute(
        "SELECT file FROM Photo WHERE fk_camera = :cam",
        {"cam": id_camera}
    )
    deja_presente = [i[0] for i in cursor.fetchall()]
    noms = [nom for nom in os.listdir(os.path.join(config.photos, dossier))
            if verification.search(nom) and os.path.join(dossier, nom) not in deja_presente]

    ids_photo = list()
    # compteur de chargement

    for nom in noms:
        img = Image.open(os.path.join(config.photos, dossier, nom))
        data = img._getexif()

        infos = {
            "id_camera": id_camera,
            "file": os.path.join(dossier, nom),
            # la date est transformee en objet datetime
            "date": datetime.strptime(data[36867], '%Y:%m:%d %H:%M:%S')
        }
        cursor.execute(ts.create_photo, infos)
        ids_photo.append(cursor.lastrowid)


def create_ind(cursor, data):
    """cree un nouvel individu et lui assigne des animaux """

    animals = data.pop("animaux")
    cursor.execute(ts.create_ind, data)
    id_ind = cursor.lastrowid
    for anim in animals:
        cursor.execute(ts.update_animal, {"id": anim, "ind": id_ind})


def init_photo(cursor):
    """
    Parcours le dossier des photos et retourne les instructions
    pour les incorporer dans la base de donnee.
    """
    # ## selection des ficher se terminant par ".jpg" ou ".JPG"
    dossiers = [nom for nom in os.listdir(config.photos)
                if os.path.isdir(os.path.join(config.photos, nom))]
    # ## extraction des informations importantes
    total = len(dossiers)
    i = 0
    for dossier in dossiers:
        print("creation base photo: {}/{}".format(i, total))
        create_photo(cursor, dossier)
        i += 1


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


def init_serie(cursor):
    """
    remplis la colonne serie de la table Photo
    """

    # on selectionne les cameras qui ont de nouvelles photos

    cursor.execute("SELECT fk_serie, fk_camera From Photo")
    result = cursor.fetchall()
    cameras = {i[1] for i in result if i[0] is None}
    print(cameras)
    #infos sur l'avancement
    total = len(cameras)
    state = 0
    for cam in list(cameras):
        print("Create series: {}/{}".format(state, total))
        state += 1
        # On detruit toutes les serie de la camera
        if cam in cursor.execute("SELECT fk_camera FROM Serie").fetchall():
            print("deletion cam: {}".format(cam))
            cursor.execute("DELETE FROM Serie WHERE fk_camera=:cam", {"cam": cam})
        # On recupere date, id_photo dans l'ordre chronologique
        cursor.execute(ts.select_date_photo_camera, {"id_camera": cam})
        photo = cursor.fetchall()

        list_serie = [[photo[0]]]
        for i in range(1, len(photo)):
            pic = photo[i]
            if (pic[0]-list_serie[-1][-1][0] > config.interval_photo):
                list_serie.append(list())
            list_serie[-1].append(pic)

        for serie in list_serie:
            cursor.execute(ts.create_serie, {
                "camera": cam, "debut": serie[0][0], "fin": serie[-1][0]
            })

            id_s = cursor.lastrowid
            for date, id_p in serie:
                cursor.execute(ts.update_photo, {"serie": id_s, "id": id_p})



def affichage_series(cursor):
    """
    Permet de fournir les variables qui permettent l'affichage des series.
    """
    cursor.execute(ts.select_serie)
    a_afficher = dict()

    series = [i for i in cursor.fetchall()]
    # serie = [id, camera, debut, fin, nombre d'animaux deja present]
    # liste des cameras
    a_afficher["cameras"] = sorted(list(set([s[1] for s in series])))
    # liste des dates
    a_afficher["dates"] = sorted(list(set([str(s[2].date()) for s in series])))
    # chaque serie a une coordonnee date/camera
    a_afficher["cellules"] = dict()
    for coord in itertools.product(a_afficher["dates"], a_afficher["cameras"]):
        a_afficher["cellules"][coord] = list()
        for s in series:
            if s[1] == coord[1] and str(s[2].date()) == coord[0]:
                # on extrait le nombre d'animaux deja present
                # dans chaque serie
                cursor.execute(ts.nb_animaux, {"id": s[0]})
                a_afficher["cellules"][coord].append({
                    "id": s[0],
                    "debut": str(s[2].time()),
                    "fin": str(s[3].time()),
                    "nb_animaux": cursor.fetchone()[0]
                    })
    return a_afficher


def affichage_photos(cursor, id_serie):
    affichage = dict(photos=list())
    # on commence par l'id et le chemin vers chaque photo
    cursor.execute(ts.select_photo, {"id_serie": id_serie})

    for id, chem in cursor.fetchall():
        affichage["photos"].append((
            int(id),
            chem
        ))
    return affichage


def affichage_animaux(cursor, id_animaux):
    animaux = []
    for id in id_animaux:
        cursor.execute(ts.afficher_animaux, {"id": id})
        animaux += cursor.fetchall()
    # animaux : fk_individu, model, id_animal, fk_serie, file, date
    classe = dict()
    for anim in animaux:
        indiv = classe.setdefault(anim[0], dict())
        model = indiv.setdefault(anim[1], dict())
        id_anim = model.setdefault(anim[2], dict())
        series = id_anim.setdefault("series", list())
        if anim[3] not in series:
            series.append(anim[3])
        photos = id_anim.setdefault("photos", list())
        photos.append({"file": anim[4], "date": anim[5]})
    return classe



def definition_html(cursor):
    """
    Permet de construire les formulaire de definition d'un animal
    pour chaque espece.
    """
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


def enregistrer_animaux(cursor, animaux, id_serie):
    """
    animaux: de la forme [{id_e: x, photos:[x,x,x], modalites:[x,x,x,x,x]}...]
    """

    # on commence par supprimer les precedents enregistrements
    #  qui ont eventuellement eu lieu sur les photos
    cursor.execute(ts.detruire_animal_sur_photo, {"id_serie": id_serie})
    cursor.execute(ts.detruire_pointer_sur_photo, {"id_serie": id_serie})

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
    """
    Renvoie la liste qui permet de caracteriser in animal avec les
    id de l'espece, des modalites, des photos liees a cet animal
    """
    cursor.execute(ts.extract_animal_serie, {"id_serie": serie})
    animaux = [i for i in cursor.fetchall()]
    result = list()
    for id in animaux:
        # les photos
        cursor.execute(
            "SELECT fk_photo FROM Pointer WHERE fk_animal=?", id
        )
        photos = [i[0] for i in cursor.fetchall()]
        # les modalites
        cursor.execute(
            "SELECT fk_modalite FROM Caracteriser WHERE fk_animal=?", id
        )
        modalites = [i[0] for i in cursor.fetchall()]
        # l'espece
        cursor.execute(
            "SELECT fk_espece FROM Animal WHERE id_animal=?", id
        )
        esp = cursor.fetchall()
        result.append({
            "id": esp[0],
            "photos": photos,
            "modalites": modalites
        })
    return result


if __name__ == "__main__":
    conn = sqlite3.connect(config.base, detect_types=config.detect_types)
    cursor = conn.cursor()

    print(charger(cursor, 1))

    conn.commit()
    conn.close()
