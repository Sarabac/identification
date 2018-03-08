library("RSQLite")
setwd("~/Dropbox/Stage2A/amphibiens/Catalogue/identification")
source("analyse.r")

data = select_modalites("grenouille")

deconnection()
