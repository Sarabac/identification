#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3
import os
import config
import gestion
from flask import Flask, render_template, jsonify

# a retirer
from especes import chevreuil

# #### Creation de la base de donnee


def lancer():
    # on verifie si la base n'existe pas deja
    first = not os.access(config.base, os.R_OK)

    conn = sqlite3.connect(config.base, detect_types=config.detect_types)
    cursor = conn.cursor()

    # si elle n'existe pas, on l'initialise
    if first:
        gestion.init_base(cursor)
        gestion.init_photo(cursor)
        gestion.init_especes(cursor)
        gestion.init_serie(cursor)
        # on enregistre les modifications
        conn.commit()

    app = application(cursor)
    app.run()
    # ne pas oublier de fermer la base
    conn.close()
    # #### Creation de l'application


def application(cursor):
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return "Hello World"

    @app.route("/series")
    def liste_series():
        a_afficher = gestion.affichage_series(cursor)
        return render_template("series.html.j2", **a_afficher)

    @app.route("/serie/<int:id_serie>")
    def etude_series(id_serie):
        a_afficher = gestion.affichage_photos(cursor, id_serie)
        return render_template("photos.html.j2", **a_afficher)

        return "num {}".format(id_serie)

    @app.route("/especes")
    def donne_especes():
        retour = jsonify(especes=gestion.get_espece(cursor))
        print(retour)
        return retour

    return app

if __name__ == "__main__":
    lancer()
