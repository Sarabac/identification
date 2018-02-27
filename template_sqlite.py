# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 08:16:45 2018

@author: luxis
"""

creation = """
CREATE TABLE 'User' (
'id_user' INTEGER,
'pseudo' TEXT,
'pw'	TEXT,
PRIMARY KEY(id_user)
);
CREATE TABLE 'Pointer' (
'fk_photo'	INTEGER,
'fk_animal'	INTEGER,
'X'	REAL,
'Y'	REAL,
'date_pointage'	timestamp,
FOREIGN KEY(fk_photo) REFERENCES Photo(id_photo),
FOREIGN KEY(fk_animal) REFERENCES Animal(id_animal)
);
CREATE TABLE 'Photo' (
'id_photo'	INTEGER ,
'file' TEXT UNIQUE,
'date'	timestamp,
'fk_camera'	INTEGER,
'fk_serie' INTEGER,
PRIMARY KEY(id_photo),
FOREIGN KEY(fk_camera) REFERENCES Camera ( id_camera ),
FOREIGN KEY(fk_serie) REFERENCES Serie ( id_serie )
);

CREATE TABLE 'Modalite' (
'id_modalite'	INTEGER ,
'nom_modalite'	TEXT,
'fk_caractere'	INTEGER,
PRIMARY KEY(id_modalite),
FOREIGN KEY(fk_caractere) REFERENCES Caractere(id_caractere)
);
CREATE TABLE 'Espece' (
'id_espece' INTEGER,
'nom_espece'	TEXT,
PRIMARY KEY(id_espece)
);
CREATE TABLE 'Caracteriser' (
'fk_animal'	INTEGER,
'fk_caractere'	INTEGER,
'ref_modalite'	INTEGER,
FOREIGN KEY(fk_animal) REFERENCES Animal(id_animal),
FOREIGN KEY(fk_caractere) REFERENCES Caractere(id_caractere)
);
CREATE TABLE "Caractere" (
'id_caractere'	INTEGER ,
'nom_caractere'	TEXT,
'fk_espece'	INTEGER,
PRIMARY KEY(id_caractere),
FOREIGN KEY(fk_espece) REFERENCES Espece ( id_espece )
);
CREATE TABLE 'Camera' (
'id_camera'	INTEGER ,
'marque'	TEXT,
'model'	TEXT,
PRIMARY KEY(id_camera),
UNIQUE (marque, model)
);
CREATE TABLE 'Animal' (
'id_animal'	INTEGER,
'date_entree' INTEGER,
'fk_espece'	INTEGER,
'fk_user'	INTEGER,
PRIMARY KEY(id_animal),
FOREIGN KEY(fk_espece) REFERENCES Espece(id_espece),
FOREIGN KEY(fk_user) REFERENCES User(id_user)
);
CREATE TABLE 'Serie'(
id_serie INTEGER,
fk_camera INTEGER,
date_debut timestamp,
date_fin timestamp,
PRIMARY KEY (id_serie),
FOREIGN KEY (fk_camera) REFERENCES Camera(id_camera)
);
"""

create_camera = """
INSERT OR IGNORE INTO Camera (marque, model) VALUES (:marque, :model);
"""
create_photo = """
INSERT INTO Photo (file, date, fk_camera) VALUES (:file, :date, (
SELECT id_camera FROM Camera
WHERE Camera.marque = :marque AND Camera.model = :model)
);
"""
create_espece = """
INSERT INTO Espece (nom_espece) VALUES (:espece);
"""
create_caractere = """
INSERT INTO Caractere (nom_caractere, fk_espece) VALUES (:nom, :espece);
"""
create_modalite = """
INSERT INTO Modalite (nom_modalite, fk_caractere) VALUES (:nom, :id_caractere);
"""

update_photo = """
UPDATE Photo SET fk_serie = :serie WHERE id_photo = :id;
"""

select_date_photo = """
SELECT date, fk_camera, id_photo FROM Photo ORDER BY fk_camera, date;
"""

create_serie = """
INSERT INTO 	Serie(id_serie, fk_camera, date_debut, date_fin)
VALUES (:id, :camera, :debut, :fin);
"""

select_serie = """
SELECT id_serie, model , date_debut, date_fin FROM Serie
INNER JOIN Camera ON Serie.fk_camera = Camera.id_camera;
"""

select_photo = """
SELECT id_photo, file FROM photo
WHERE fk_serie = :id_serie;
"""

colonnes_distinctes = """
SELECT DISTINCT {col} FROM {tab} ORDER BY {col};
"""

ajax_get_espece = """
SELECT Espece.id_espece, Espece.nom_espece,
Caractere.id_caractere, Caractere.nom_caractere,
Modalite.id_modalite, Modalite.nom_modalite
FROM Espece
LEFT JOIN Caractere ON fk_espece = id_espece
LEFT JOIN Modalite ON fk_caractere = id_caractere;
"""
