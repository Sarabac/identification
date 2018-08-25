current_path <- rstudioapi::getActiveDocumentContext()$path 
# The next line set the working directory to the relevant one:
setwd(dirname(current_path ))

source("analyse.r")

photos_faites = dbGetQuery(cursor, "SELECT id_photo FROM Photo INNER JOIN Pointer ON id_photo = fk_photo")

fait = length(unique(photos_faites$id_photo))
total = dbGetQuery(cursor, "SELECT id_photo FROM Photo")$id_photo
