#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#not finished

list_especes = ["chevreuil", "sanglier"]
especes = {e:dict() for e in list_especes}

def deco(fonc):
    def wrapper(*arg, **kwd):
        result = fonc(*arg, **kwd)
        return [i[0] for i in result]




def male_chevreuils(cursor):
    instr = """SELECT id_animal FROM animal
            INNER JOIN Caracteriser ON fk_animal = id_animal
            INNER JOIN Modalite ON fk_modalite = id_modalite
            INNER JOIN Caractere ON fk_caractere = id_caractere
            WHERE nom_caractere = "bois" AND nom_modalite NOT IN ('abscents') """
    cursor.execute(instr)
    return [i[0] for ]
