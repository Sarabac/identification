# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 21:22:16 2018

@author: luxis
"""
import os
import sqlite3
from datetime import timedelta

# ### chemin vers les dossier #####
# ## s'ecrit sout la forme :
# os.path.join("dossier", "sous_dossier", "sous_sous_dossier")
photos = os.path.join("static", "photos")
base = os.path.join("chevreuil.db")
template = os.path.join("template")

# ## interval maximum entre les photos pour former une serie
# ## s'ecrit sous la forme timedelta(jours, secondes, microsecondes)
# ## les microseconde sont inutiles
interval_photo = timedelta(0, 60)

# #### Ne pas changer ######
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
# #### whath
