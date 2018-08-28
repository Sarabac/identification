# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 08:16:45 2018

@author: luxis
"""
# construction des differentes tables de la base de donnee
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
FOREIGN KEY(fk_photo) REFERENCES Photo(id_photo) ON DELETE CASCADE,
FOREIGN KEY(fk_animal) REFERENCES Animal(id_animal) ON DELETE CASCADE
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
'fk_modalite'	INTEGER,
FOREIGN KEY(fk_animal) REFERENCES Animal(id_animal) ON DELETE CASCADE,
FOREIGN KEY(fk_modalite) REFERENCES Modalite(id_modalite) ON DELETE CASCADE
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
'fk_individu'	INTEGER,
PRIMARY KEY(id_animal),
FOREIGN KEY(fk_espece) REFERENCES Espece(id_espece),
FOREIGN KEY(fk_user) REFERENCES User(id_user),
FOREIGN KEY(fk_individu) REFERENCES Individu(id_individu)
);
CREATE TABLE 'Individu' (
'id_individu'	INTEGER ,
'nom_individu'	TEXT,
'commentaire'	TEXT,
PRIMARY KEY(id_individu)
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

# son creer une nouvelle camera si une autre ne possede pas le meme nom
create_camera = """
INSERT OR IGNORE INTO Camera (marque, model) VALUES (:marque, :model);
"""
# a partir des cameras, on associe les differentes photos qu'elle a produit
create_photo = """
INSERT INTO Photo (file, date, fk_camera) VALUES (:file, :date, :id_camera);
"""
# les nouvelles especes
create_espece = """
INSERT INTO Espece (nom_espece) VALUES (:espece);
"""
# associe les differents caracteres aux especes
create_caractere = """
INSERT INTO Caractere (nom_caractere, fk_espece) VALUES (:nom, :espece);
"""
# associe les differentes modalites aux caracteres
create_modalite = """
INSERT INTO Modalite (nom_modalite, fk_caractere) VALUES (:nom, :id_caractere);
"""
# on associe apres coup chaque photo a une serie
update_photo = """
UPDATE Photo SET fk_serie = :serie WHERE id_photo = :id;
"""

select_date_photo = """
SELECT date, fk_camera, id_photo FROM Photo ORDER BY fk_camera, date;
"""
select_date_photo_camera = """
SELECT date, id_photo FROM Photo WHERE fk_camera = :id_camera
ORDER BY date;
"""

create_serie = """
INSERT INTO 	Serie(fk_camera, date_debut, date_fin)
VALUES (:camera, :debut, :fin);
"""

select_serie = """
SELECT Serie.id_serie, Camera.model ,
Serie.date_debut, Serie.date_fin FROM Serie
INNER JOIN Camera ON Serie.fk_camera = Camera.id_camera;
"""
nb_animaux = """
SELECT COUNT(Pointer.fk_photo) FROM Serie
INNER JOIN Photo ON Photo.fk_serie = Serie.id_serie
INNER JOIN Pointer ON Photo.id_photo = Pointer.fk_photo
WHERE Serie.id_serie = :id;
"""

select_photo = """
SELECT id_photo, file FROM Photo
WHERE fk_serie = :id_serie
ORDER BY datetime(date) DESC;
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

detruire_animal_sur_photo = """
DELETE FROM Animal WHERE id_animal IN (
SELECT DISTINCT fk_animal FROM Pointer INNER JOIN Photo ON fk_photo = id_photo
INNER JOIN Serie ON fk_serie = :id_serie
);
"""

detruire_pointer_sur_photo = """
DELETE FROM Pointer WHERE fk_animal IN (
SELECT DISTINCT fk_animal FROM Pointer INNER JOIN Photo ON fk_photo = id_photo
INNER JOIN Serie ON fk_serie = :id_serie
);
"""

create_animal = """
INSERT INTO Animal(fk_espece, date_entree)
VALUES (:fk_espece, :date_entree);
"""
extract_animal_serie = """
SELECT DISTINCT id_animal FROM Serie INNER JOIN Photo ON id_serie=fk_serie
INNER JOIN Pointer ON id_photo=fk_photo
INNER JOIN Animal ON id_animal=fk_animal
WHERE id_serie=:id_serie;
"""
pointer = """
INSERT INTO Pointer(fk_photo, fk_animal)
VALUES (:fk_photo, :fk_animal);
"""
caracteriser = """
INSERT INTO Caracteriser(fk_modalite, fk_animal)
VALUES (:fk_modalite, :fk_animal);
"""

espece_on_photo = """
SELECT Camera.model, Espece.nom_espece, Photo.file FROM Camera
INNER Join Photo On id_camera=fk_camera
INNER JOIN Pointer On id_photo=fk_photo
INNER JOIN Animal On id_animal=fk_animal
INNER JOIN Espece On id_espece=fk_espece
"""
