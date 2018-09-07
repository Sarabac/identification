#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3
import os
import config
import gestion
from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import webbrowser
import template_sqlite as ts
from filtres import filtres
# #### Creation de la base de donnee

def create_conn():
    conn = sqlite3.connect(config.base, detect_types=config.detect_types)
    cursor = conn.cursor()
    return (cursor, conn)


def lancer():
    # on verifie si la base n'existe pas deja
    first = not os.access(config.base, os.R_OK)

    cursor, conn = create_conn()
    cursor.execute("""PRAGMA foreign_keys = ON""")

    # si elle n'existe pas, on l'initialise
    if first:
        gestion.init_base(cursor)
        gestion.init_especes(cursor)
    # on reinitialise a chaque fois les photos et series
    # pour integrer d'eventuelles nouvelles photos
    gestion.init_photo(cursor)
    conn.commit()
    gestion.init_serie(cursor)
    # on enregistre les modifications
    conn.commit()

    app = application(cursor, conn)
    app.run()

    # ne pas oublier de fermer la base
    conn.close()
    # #### Creation de l'application


def application(cursor, conn):
    app = Flask(__name__)

    @app.route('/')
    def index():
        cursor, conn = create_conn()
        return render_template("index.html.j2", filtres=filtres)

    @app.route("/series")
    def liste_series():
        cursor, conn = create_conn()
        a_afficher = gestion.affichage_series(cursor)
        return render_template("series.html.j2", **a_afficher)

    @app.route("/serie/<int:id_serie>")
    def etude_series(id_serie):
        cursor, conn = create_conn()
        ficher = gestion.affichage_photos(cursor, id_serie)
        definition = gestion.definition_html(cursor)
        param = dict(ficher, serie=id_serie, **definition)
        param = dict(
            param,
            chargement=json.dumps(gestion.charger(cursor, id_serie))
        )
        return render_template("photos.html.j2", **param)

    @app.route("/filtre/<nom_espece>/<nom_filtre>")
    def etude_animaux(nom_espece, nom_filtre):
        cursor, conn = create_conn()
        animaux = filtres[nom_espece][nom_filtre](cursor)
        indivs = gestion.affichage_animaux(cursor, animaux)
        print(indivs)

        return render_template("animals.html.j2", individus=indivs)

    @app.route("/enregistrer/<int:id_serie>", methods=["POST"])
    def enregistrer(id_serie):
        cursor, conn = create_conn()
        donnees = json.loads(request.get_data().decode())
        # de la forme : [{id_e: x, photos:[x,x,x], modalites:[x,x,x,x,x]}...]

        gestion.enregistrer_animaux(cursor, donnees, id_serie)
        conn.commit()
        return jsonify(status="ok")

    webbrowser.open("http://127.0.0.1:5000/")

    @app.route("/creer_ind", methods=["POST"])
    def creer_ind():
        cursor, conn = create_conn()
        donnees = json.loads(request.get_data().decode())
        # de la forme : {'animaux': [1422, 775],
        #   'commentaire': 'asdasdasdasdas', 'nom': 'asdas'}
        verif = any([type(i) is int for i in donnees["animaux"]])
        verif = verif and bool(donnees["commentaire"])
        verif = verif and bool(donnees["nom"])
        if verif:
            gestion.create_ind(cursor, donnees)
            stat = "ok"
        else:
            stat = "fail"
        conn.commit()
        return jsonify(status=stat)

    @app.route('/static-photos/<path:filename>')
    def send_photo(filename):
        return send_from_directory(config.photos, filename)

    return app


if __name__ == "__main__":
    lancer()


test = False
if test:
    cursor, conn = create_conn()
    f = """CREATE TABLE 'Individu' ('id_individu'	INTEGER ,'nom_individu'	TEXT,'commentaire'	TEXT,PRIMARY KEY(id_individu));"""
    cursor.execute(p)
    p = "ALTER TABLE Animal ADD COLUMN 'fk_individu'	INTEGER"
    conn.commit()
