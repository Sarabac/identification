#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3
import os
import config
import gestion
from flask import Flask, render_template, request, jsonify
import json
import webbrowser
import pdb
# #### Creation de la base de donnee

def create_conn():
    conn = sqlite3.connect(config.base, detect_types=config.detect_types)
    cursor = conn.cursor()
    return (cursor,conn)


def lancer():
    # on verifie si la base n'existe pas deja
    first = not os.access(config.base, os.R_OK)

    conn = sqlite3.connect(config.base, detect_types=config.detect_types)
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")

    # si elle n'existe pas, on l'initialise
    if first:
        gestion.init_base(cursor)
        gestion.init_especes(cursor)
    # on reinitialise a chaque fois les photos et series
    # pour integrer d'eventuelles nouvelles photos
    gestion.init_photo(cursor)
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

    @app.route("/enregistrer", methods=["POST"])
    def enregistrer():
        cursor, conn = create_conn()
        donnees = json.loads(request.get_data().decode())
        # de la forme : [{id_e: x, photos:[x,x,x], modalites:[x,x,x,x,x]}...]
        gestion.enregistrer_animaux(cursor, donnees)
        conn.commit()
        return jsonify(status="ok")

    webbrowser.open("http://127.0.0.1:5000/")

    return app

if __name__ == "__main__":
    lancer()
