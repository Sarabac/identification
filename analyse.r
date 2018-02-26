library("RSQLite")

#connection a la base de donnee
drv <- SQLite()
cursor <- dbConnect(drv, dbname="chevreuil.db")
# requete
query = dbSendQuery(conn = cursor, "SELECT * FROM Photo")
# conversion en data frame
donn = dbFetch(query, n = -1)
