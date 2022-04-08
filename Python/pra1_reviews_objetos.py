# Webscraping
# Análisis comentarios Google Maps y Tripadvisor 
# Dataset para NLP análisis de sentimientos
# PRA1 Tipología Ciclo de Datos
# Francisco José Ramírez

from importlib.resources import path
import os
import csv
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import urllib
import urllib.request

# Definimos los XPATH principales de los elementos a recuperar la información
# Se eligen dos páginas web donde aparecen comentarios positivos o negativos

# XPATHs TripAdvisor Restaurantes
#main_xpath = "//span[@class='taLnk ulBlueLinks']"
rest_find_xpath = ".//div[@class='review-container']"
rest_titulo_xpath=".//span[@class='noQuotes']"
rest_fecha_xpath=".//span[contains(@class, 'ratingDate')]"
rest_puntuacion_xpath=".//span[contains(@class, 'ui_bubble_rating bubble_')]"
rest_comentario_xpath=".//p[@class='partial_entry']"

# XPATHS Google Reviews Restaurantes (puede servir para otros)
google_find_xpath = "//div/div[@data-review-id]"
google_puntuacion_class = 'ODSEW-ShBeI-H1e3jb'
google_comentario_class = 'ODSEW-ShBeI-text'

class Dataset_Comentarios(object):
    
    def __init__(self, web_objetivo):
        self.objectivo=web_objetivo      

    def boton_privacidad_trip(self):
        try:    
            time.sleep(3)
            boton_aceptar = driver.find_element_by_id("onetrust-accept-btn-handler")
            driver.execute_script("arguments[0].click();", boton_aceptar)
        except:
            return

    def boton_privacidad_google(self):
        try:    
            time.sleep(3)
            boton_aceptar = driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/input[11]")
            driver.execute_script("arguments[0].click();", boton_aceptar)
        except:
            return

    def puntuacion_sentimiento_google(self, puntos):
        # En función de la puntuación determinaremos los siguientes varemos de sentimientos:
        # 0 a 2 Negativo
        # 2 a 3 Neutral
        # 3 a 5 Bueno
        sentimiento = ""
        if puntos in range(0,2):
            sentimiento = "negativo"
        elif puntos in range(2,3):
            sentimiento = "neutral"
        elif puntos in range(3,6):
            sentimiento = "positivo"
        return(sentimiento)

    def puntuacion_sentimiento_trip(self, puntos):
        # En función de la puntuación determinaremos los siguientes varemos de sentimientos:
        # 0 a 20 Negativo
        # 20 a 30 Neutral
        # 30 a 50 Bueno
        sentimiento = ""
        if puntos in range(0,20):
            sentimiento = "negativo"
        elif puntos in range(20,30):
            sentimiento = "neutral"
        elif puntos in range(30,60):
            sentimiento = "positivo"
        return(sentimiento)


    def fichero_comentarios(self, nombre):
        path_actual = os.getcwd()
        os.chdir(path_actual)
        # fichero csv para almancenar los comentarios
    
        ficherocsv = open(nombre, 'w', encoding="utf-8-sig")
        fichero_output = csv.writer(ficherocsv, delimiter=';')
        # Añado cabecera al csv
        fichero_output.writerow(["puntuación", "review","sentimiento"])   
        return(fichero_output)      


    def comentarios_tripadvisor_restaurantes(self, npaginas, fichero_salida):
        # Recorremos las páginas definidas
        for npag in range(0, npaginas):
            # abrimos los comentarios
            # Damos un tiempo de espera para que se abra
            time.sleep(4)
            #driver.find_element_by_xpath(main_xpath).click()
            container_review = driver.find_elements_by_xpath(rest_find_xpath)
            # Ahora recorremos todos los comentarios
            for comentarios in range(len(container_review)):
                puntuacion = container_review[comentarios].find_element_by_xpath(rest_puntuacion_xpath).get_attribute("class").split("_")[3]
                puntos_sentimiento = self.puntuacion_sentimiento_trip(int(puntuacion))
                comentario = container_review[comentarios].find_element_by_xpath(rest_comentario_xpath).text.replace("\n", " ")
                # Almacenamos la salida en el fichero asignado
                fichero_salida.writerow([puntuacion, comentario, puntos_sentimiento])
            # Click Siguiente página hasta fin bucle npaginas:
            button = driver.find_element_by_xpath('.//a[@class="nav next ui_button primary"]')
            driver.execute_script("arguments[0].click();", button)    


    def comentarios_google_reviews(self, fichero_salida):
        # Expandimos los resultados de las reviews
        time.sleep(3)
        # Hacemos click en el botón más reseñas para mostrar más comentarios y almacenarlos
        driver.find_element_by_xpath('//button[starts-with(@aria-label,"Más reseñas")]').click()
        # Recorremos las páginas definidas
        time.sleep(4)
        container_review = driver.find_elements_by_xpath(google_find_xpath)
        for comentarios in range(len(container_review)):
            puntuacion = container_review[comentarios].find_element_by_class_name(google_puntuacion_class).get_attribute("aria-label").split(" ")[1]
            comentario = container_review[comentarios].find_element_by_class_name(google_comentario_class).text
            puntos_sentimiento= self.puntuacion_sentimiento_google(int(puntuacion))
            fichero_salida.writerow([puntuacion, comentario, puntos_sentimiento])
        print("Comentarios extraidos:", len(container_review))


if __name__ == "__main__":
    
    # Parámetros generales
    # Ajustamos las opciones de acceso para evitar problemas legales y de bloqueo
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito") 
    option.add_argument("user-agent=AcademicCrawler")
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
    # Fichero para almacenar todos los comentarios
    nombrefile_tripadvisor="dataset_tripadvisor.csv"

    # Visualizamos el fichero robots.txt para su análisis
    #robots = tripadvisor.get_robots("https://www.tripadvisor.es/robots.txt")
    #print(robots)

    print("Google Maps Reviews")

    # Google Maps Reviews
    #####################
    nombrefile_googlemaps="dataset_googlemaps.csv"
    website="https://www.google.com/maps/"
    url_googlemaps = "https://www.google.com/maps/place/Restaurante+La+Pepica/@39.4634132,-0.3252193,17z/data=!3m1!4b1!4m5!3m4!1s0xd6048422f04f9ef:0xf8470a431cc0fe26!8m2!3d39.4634132!4d-0.3230306"
    googlemaps = Dataset_Comentarios(website)
    driver.get(url_googlemaps)
    googlemaps.boton_privacidad_google()
    fichero_resultados=googlemaps.fichero_comentarios(nombrefile_googlemaps)
    googlemaps.comentarios_google_reviews(fichero_resultados)

    print("Tripadvisor")

    # TripAdvisor Reviews
    #####################
    # Número de páginas a comprobar los comentarios TripAdvisor
    paginas = 2
    nombrefile_tripadvisor="dataset_tripadvisor.csv"
    # URL TripAdvisor a comprobar
    website="https://tripadvisor.es/"
    url_tripadvisor = "https://www.tripadvisor.es/Restaurant_Review-g187457-d1026118-Reviews-Bully-San_Sebastian_Donostia_Province_of_Guipuzcoa_Basque_Country.html"
    tripadvisor = Dataset_Comentarios(website)
    driver.get(url_tripadvisor)
    # Aceptamos las condiciones del mensaje de cookies y privacidad
    tripadvisor.boton_privacidad_trip()
    fichero_resultados=tripadvisor.fichero_comentarios(nombrefile_tripadvisor)
    tripadvisor.comentarios_tripadvisor_restaurantes(paginas,fichero_resultados)
   
    driver.quit()

    print("Fin webscraping")