#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def execinstr(instr):
    def funct(cursor):
        cursor.execute(instr)
        return [i[0] for i in cursor.fetchall()]
    return funct



class calldb(dict):

    def __call__(self, espece, instr, name=None):
        if espece not in self.keys():
            self[espece] = dict()
        if type(instr) is type(execinstr) and name is None:
            name = instr.__name__
        if type(instr) is str:
            instr = execinstr(instr)
        self[espece][name] = instr

filtres = calldb()


### creation des filtre
male_chevreuils = """
    SELECT id_animal FROM animal
    INNER JOIN Caracteriser ON fk_animal = id_animal
    INNER JOIN Modalite ON fk_modalite = id_modalite
    INNER JOIN Caractere ON fk_caractere = id_caractere
    WHERE nom_caractere = "bois" AND nom_modalite NOT IN ('abscents')
    """

oiseaux = """
    SELECT id_animal FROM animal
    INNER JOIN Espece ON fk_espece = id_espece
    WHERE nom_espece IN ('oiseau')
    """

filtres("chevreuil", male_chevreuils, "male_chevreuils")
filtres("oiseau", oiseaux, "oiseaux")
