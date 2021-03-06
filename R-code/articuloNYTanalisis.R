---
title: "Examen de un art�culo del New York Times"
author: "ANTONIO SANCHEZ NAVARRO"
date: "19 de octubre de 2018"
output: html_document
---

```{r chumck1}

# Este script de c�digo R realiza web scraping a una p�gina web que recoge un art�culo del New York Times
# titulado "Trump's lies". Los datos que se recogen son la fecha de la mentira, la mentira en si, una explicaci�n
# de por qu� se ha detectado la mentira y una URL a un art�culo que apoya la justificaci�n (incrustada en el texto).
#Espero que el resultado obtenido sea de vuestro agrado.

# Carga de paquetes y uso de librer�as
install.packages("rvest")
install.packages("stringr")
install.packages("dplyr")
install.packages("lubridate")
install.packages("readr")
install.packages("xml2")
library(rvest)
library(stringr)
library(dplyr)
library(lubridate)
library(readr)

# Leyendo la p�gina web en R. Usamos el paquete rvest, que facilita el rastreo de datos de p�ginas web html.
# La funci�n read_html() nos devuelve un documento XML con toda la informaci�n sobre la p�gina web

webpage <- read_html("https://www.nytimes.com/interactive/2017/06/23/opinion/trumps-lies.html")
# Inspeccionamos la p�gina web semilla
webpage

# Recopilaci�n de todos los registros. 
# Dada la estructura en HTML de los registros, para recopilarlos es necesario identificar todas las etiquetas <span>
# que pertenecen a class = "short-desc". La funci�n que permite hacerlo es html_nodes(), que precisa el documento XML
# le�do y los nodos que queremos seleccionar. Descubrimos que todos los registros se pueden seleccionar usando el
# selector ".short-desc"

results <- webpage %>% html_nodes(".short-desc")  #Usamos el %>% pipe-operator del paquete magrittr
results

# Construyendo el dataset

records <- vector("list", length = length(results))

for (i in seq_along(results)) {
  
    # Obtenemos las fechas de los registros
    # Como est�n incrustadas en la etiqueta <strong>, usamos html_nodes() con el selector "Strong" para seleccionarlas
    # La funci�n html_text() extrae s�lo el texto, con el argumento de recorte activo para recortar espacios iniciales
    # y finales

    date <- str_c(results[i] %>% 
                      html_nodes("strong") %>% 
                      html_text(trim = TRUE), ', 2017') 
    
    # Obtenemos las mentiras de cada uno de los registros
    # Usamos la funci�n xml_contents () del paquete xml2, que nos devuelve una lista con los nodos que forman parte de
    # first_result
    
    lie <- str_sub(xml_contents(results[i])[2] %>% html_text(trim = TRUE), 2, -2)
    # Obtenemos las justificaciones para cada uno de los registros (por qu� se ha mentido)
    # Seleccionamos el texto dentro de la etiqueta <span> que pertenece a class = ". short-truth"
    
    explanation <- str_sub(results[i] %>% 
                               html_nodes(".short-truth") %>% 
                               html_text(trim = TRUE), 2, -2)
    
    # Obtenemos la URL de cada registro
    # Seleccionamos el nodo con la etiqueta <a> con la funci�n html_nodes () y luego seleccionamos el atributo href
    # con la funci�n html_attr ()

    url <- results[i] %>% html_nodes("a") %>% html_attr("href")
    records[[i]] <- data_frame(FECHA = date, MENTIRA = lie, EXPLICACION = explanation, URL = url)
}

df <- bind_rows(records)
glimpse(df)

# Transformamos el dataset con el formato de fecha adecuado
df$FECHA <- mdy(df$FECHA)

# Observamos la cabecera del dataset
head(df)
# Exportamos el dataset a un fichero CSV en la ruta especificada
write.csv(df, file="C:/Users/tonis/Desktop/UOC/Tipolog�a y ciclo de vida de los datos/WEB SCRAPING/articuloNYTanalisis.csv")
```