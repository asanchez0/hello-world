# -*- coding: cp1252 -*-
# Descargamos el sitio web HTML de interés en Python, usando la librería requests.
import requests  
r = requests.get('https://www.nytimes.com/interactive/2017/06/23/opinion/trumps-lies.html')
# Imprimimos los primeros 500 caracteres del documento HTML

# Parseamos el contenido bruto del HTML usando la librería Beautiful Soup 4 (Beautiful Soup lee el HTML y da un sentido a su estructura)
# El resultado lo almaceno en un nuevo objeto, al que llamo soup:
from bs4 import BeautifulSoup  
soup = BeautifulSoup(r.text, 'html.parser')  
# Pedimos a la librería Beautiful Soup que nos encuentre todos los registros:
results = soup.find_all('span', attrs={'class':'short-desc'})
# Podemos comprobar la longitud de results:

# Dividimos el objeto como si fuera una lista, para exaninar los tres primeros resultados:

# Comprobamos que el último objeto coincide con el del artículo

# Construcción del dataset. Almaceno la salida del bucle en una lista de filas llamada records
records = []  
for result in results:  
    date = result.find('strong').text[0:-1] + ', 2017'
    lie = result.contents[1][1:-2]
    explanation = result.find('a').text[1:-1]
    url = result.find('a')['href']
    records.append((date, lie, explanation, url))
# Longitud del objeto records:

# Vista de los tres primeros registros:

# Damos al conjunto de datos una estructura tabular:
import pandas as pd  
df = pd.DataFrame(records, columns=['FECHA', 'MENTIRA', 'EXPLICACION', 'URL'])  
# Damos a la fecha un formato consistente:
df['FECHA'] = pd.to_datetime(df['FECHA']) 
# El método head() permite examinar los primeros registros del dataset:

# El método tail() permite examinar los últimos registros de la lista:

# Exportamos los datos a un fichero CSV, que se ubicará en el directorio desde donde residía este fichero python:
df.to_csv('articuloNYTanalisis.csv', index=False, encoding='utf-8') 