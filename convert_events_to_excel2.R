library("RSQLite")
library("dplyr")
#library("xlsx")
# the following line is for getting the path of your current open file
current_path <- rstudioapi::getActiveDocumentContext()$path 
# The next line set the working directory to the relevant one:
setwd(dirname(current_path ))
#connection a la base de donnee
cursor <- dbConnect(SQLite(), dbname="chevreuil.db")

indv = "
SELECT DISTINCT model, date_debut, nom_individu, commentaire FROM Individu
INNER JOIN Animal ON fk_individu = id_individu
INNER JOIN Pointer ON fk_animal = id_animal
INNER JOIN Photo ON fk_photo = id_photo
INNER JOIN Serie ON fk_serie = id_serie
INNER JOIN Camera ON Serie.fk_Camera = id_camera
"
cycle = as.difftime("00:05:00","%H:%M:%S") # minimum time period between each event

indiv = dbGetQuery(cursor, indv)
dbDisconnect(cursor)
donn = data.frame(Site = as.numeric(gsub("SC", "", indiv$model)),
                  Time = as.POSIXct(indiv$date_debut, "%Y-%m-%d %H:%M:%S"),
                  Sex = "m",
                  Roe_Name = indiv$nom_individu,
                  Features = indiv$commentaire,
                  Suite = 0)

donn = donn[order(donn$Time), ]



i = 0

for (a in 2:dim(donn)[1]){
  avant = donn[a-1, "Time"]
  apres = donn[a, "Time"]
  if(apres-avant > cycle){
    i = i + 1
  }
  donn[a, "Suite"] = i
}

Roe = donn %>% group_by(Site, Roe_Name, Sex, Features, Suite) %>% summarise(Time = min(Time))

#Roe = aggregate(Time ~ Site + Roe_Name + Sex + Features + Suite, donn, min )
# mauvaise conversion CEST
result = as.data.frame( Roe[, c("Site", "Time", "Sex", "Roe_Name", "Features")] )
result$Time = strftime(Roe$Time, format = "%d/%m/%Y %H:%M", tz = "GMT")

write.csv(result, "males_May_June_revised.csv", row.names = FALSE)
#write.xlsx(result, "males_May_June_revised.xlsx", row.names = FALSE) 
