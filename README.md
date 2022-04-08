# sentiment-webscraping
Generación de Datasets para el análisis de sentimientos basado en críticas de servicios    
PRA1 Webscraping

# Autor: 
Francisco José Ramírez Vicente

# Ficheros

**Francisco_Ramirez_PRA1.pdf**   
soluciones a las preguntas de la práctica

**README.md**   
este fichero

**LICENSE**   
Licencia

**dataset_googlempas.csv**          
dataset de ejemplo generado con Google Maps Reviews

**dataset_sentiment_analisys.csv**  
dataset completo, uniendo ambos, Google Maps Reviews y Tripadvisor

**dataset_tripadvisor.cvs**         
dataset extraído de Tripadvisor Restaurantes

**Python/pra1_reviews_objetos.py**         
programa principal

# DOI Zenodo
https://doi.org/10.5281/zenodo.6425686

# Requisitos de instalación y ejecución
**Windows 10/11**
**Python 3.X**

Selenium: 
*pip install selenium*

Webdriver Manager: 
*pip install webdriver-manager*

Ejecución:
*python pra1_reviews_objetos.py*

* Abrirá en primer la web de Google Maps, aceptará los términos de servicio y comenzará el scraping
* Expandirá los comentarios y se extraen las reviews
* Al cabo de unos segundos se cerrará y los datos se almacenan en el fichero CSV de GoogleMaps
* Inmediatamente después se abrirá la web de Tripadvisor
* Aceptará los términos y comenzará el scraping
* Pasará dos veces de página y se extraen las reviews
* Los datos se guardan en el fichero CSV de Tripadvisor
* Termina el proceso cerrando las ventanas
