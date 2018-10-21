__author__ = 'ANTONIO SANCHEZ NAVARRO'
# Descargamos el sitio web HTML de inter�s en Python, usando la librer�a requests.
import requests  
r = requests.get('https://www.nytimes.com/interactive/2017/06/23/opinion/trumps-lies.html')
# Imprimimos los primeros 500 caracteres del documento HTML
print(r.text[0:500])
# Parseamos el contenido bruto del HTML usando la librer�a Beautiful Soup 4 (Beautiful Soup lee el HTML y da un sentido a su estructura)
# El resultado lo almaceno en un nuevo objeto, al que llamo soup:
from bs4 import BeautifulSoup  
soup = BeautifulSoup(r.text, 'html.parser')  
# Pedimos a la librer�a Beautiful Soup que nos encuentre todos los registros:
results = soup.find_all('span', attrs={'class':'short-desc'})
# Podemos comprobar la longitud de results:
len(results)
# Dividimos el objeto como si fuera una lista, para exaninar los tres primeros resultados:
results[0:3]
# Comprobamos que el �ltimo objeto coincide con el del art�culo
results[-1]
# Construcci�n del dataset. Almaceno la salida del bucle en una lista de filas llamada records
records = []  
for result in results:  
    date = result.find('strong').text[0:-1] + ', 2017'
    lie = result.contents[1][1:-2]
    explanation = result.find('a').text[1:-1]
    url = result.find('a')['href']
    records.append((date, lie, explanation, url))
# Longitud del objeto records:
len(records) 
# Vista de los tres primeros registros:
records[0:3]
# Damos al conjunto de datos una estructura tabular:
import pandas as pd  
df = pd.DataFrame(records, columns=['FECHA', 'MENTIRA', 'EXPLICACION', 'URL'])  
# Damos a la fecha un formato consistente:
df['FECHA'] = pd.to_datetime(df['FECHA']) 
# El m�todo head() permite examinar los primeros registros del dataset:
df.head() 
# El m�todo tail() permite examinar los �ltimos registros de la lista:
df.tail()
# Exportamos los datos a un fichero CSV, que se ubicar� en el directorio desde donde resid�a este fichero python:
df.to_csv('mentiras.csv', index=False, encoding='utf-8') 