library("RSQLite")
setwd("~/github/appli_chevreuil")
source("analyse.r")

data = select_modalites("grenouille")

deconnection()
