library("RSQLite")
setwd("~/Dropbox/Stage2A/amphibiens/Catalogue/identification")
#connection a la base de donnee
cursor <- dbConnect(SQLite(), dbname="chevreuil.db")
# requete
print(getwd())
select_modalites = function(espece){
  individus = "
  SELECT DISTINCT fk_animal, date_debut FROM photo 
  INNER JOIN pointer ON fk_photo=id_photo 
  INNER JOIN Animal ON id_animal=fk_animal 
  INNER JOIN Espece ON id_espece=fk_espece 
  INNER JOIN Serie ON fk_serie=id_serie 
  WHERE nom_espece='"
  indiv = dbGetQuery(cursor, paste(individus, espece, "'", sep=""))
  # selection des caractere des grenouilles
  select_caract = "SELECT nom_caractere FROM Caractere
  INNER JOIN Espece ON id_espece=fk_espece
  WHERE nom_espece='"
  caracteres = dbGetQuery(cursor, paste(select_caract, espece, "'", sep=""))
  # insertion des modalites des caracteres des grenouilles
  indiv[caracteres$nom_caractere] = NA
  for (i in indiv$fk_animal){
    instructions = "
SELECT nom_caractere, nom_modalite FROM Animal INNER JOIN Caracteriser ON fk_animal=id_animal
LEFT JOIN Modalite ON fk_modalite=id_modalite
INNER JOIN Caractere ON fk_caractere=id_caractere
WHERE id_animal="
    modalites = dbGetQuery(cursor, paste(instructions, i, sep=""))
    indiv[indiv$fk_animal==i,modalites$nom_caractere] = modalites$nom_modalite
  }
  
  donnees = apply(indiv, 2, as.factor)
  noms_colonne = colnames(donnees)
  noms_colonne[2] = "Date"
  colnames(donnees) <- noms_colonne
  donnees = donnees[,-1]
  return(donnees)
}

liste_images = function(espece){
  
  individus = "Select id_animal, file FROM Photo 
  INNER JOIN Pointer ON id_photo = fk_photo
  INNER JOIN Animal ON id_animal = fk_animal
  INNER JOIN Espece ON id_espece = fk_espece
  WHERE nom_espece='"
  indiv = dbGetQuery(cursor, paste(individus, espece, "'", sep=""))
  return(indiv)
}

deconnection = function(){
  dbDisconnect(cursor)
}
