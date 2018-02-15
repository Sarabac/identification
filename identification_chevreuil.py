#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import sqlite3
import os
import config
import gestion
from flask import Flask, render_template

##### Creation de la base de donnee
def lancer ():
    # on verifie si la base n'existe pas deja
    first = not os.access(config.base, os.R_OK)

    conn = sqlite3.connect(config.base, detect_types = config.detect_types)
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

    #ne pas oublier de fermer la base
    conn.close()
##### Creation de l'application

def application(cursor):
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return "Hello World"

    return app

if __name__ == "__main__":
    lancer()
