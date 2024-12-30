#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 11:08:13 2024

@author: raquelyunoenbadillosalas
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import urllib.request

# Configuración del driver (asegúrate de tener el controlador correcto)
driver = webdriver.Chrome()  # Cambia a geckodriver si usas Firefox
base_url = 'https://www.inegi.org.mx'
url = 'https://www.inegi.org.mx/app/descarga/default.html'

# Carpeta de salida para los archivos descargados
output_folder = "/Volumes/Crucial X8/LEProject_finalProject/DENUE/"
os.makedirs(output_folder, exist_ok=True)

# Función para descargar un archivo con la extensión correcta
import requests

def download_file(url, output_folder):
    # Extraer el nombre del archivo de la URL
    filename = url.split("/")[-1]
    if not filename.endswith(".zip"):
        filename += ".zip"  # Asegurar que tenga la extensión correcta

    local_filename = os.path.join(output_folder, filename)

    # Verificar si el archivo ya existe
    if os.path.exists(local_filename):
        print(f"El archivo ya existe, se omite: {filename}")
        return

    # Descargar el archivo
    response = requests.get(url, verify=False)  # Ignorar verificación SSL
    if response.status_code == 200:
        with open(local_filename, "wb") as f:
            f.write(response.content)
        print(f"Descargado: {local_filename}")
    else:
        print(f"Error al descargar {filename}. Código de estado: {response.status_code}")


# Función para esperar hasta que la página esté completamente cargada
def wait_for_page_to_load(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        print("Página cargada con éxito.")
    except Exception as e:
        print("Error al cargar la página:", e)
        driver.quit()
        exit()

# Función para obtener opciones de descarga desde el HTML
def get_options(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all("a", href=True)
    options = [
        {
            "name": link.text.strip(),
            "url": base_url + link["href"]  # Construir URL absoluta
        }
        for link in links if "/contenidos/masiva/denue/" in link["href"].lower() and "_csv" in link["href"].lower()
    ]
    return options

# Descargar todos los archivos de las opciones encontradas
def download_all_options(driver, output_folder):
    options = get_options(driver)
    if not options:
        print("No se encontraron archivos para descargar.")
        return
    for option in options:
        download_file(option["url"], output_folder)

# Inicia el proceso de scraping
try:
    driver.get(url)
    driver.get(url)
    wait_for_page_to_load(driver, timeout=2)  # Espera 60 segundos para que cargue la página

    print("Buscando archivos de 2024...")
    time.sleep(5)  # Espera adicional para asegurar que la página esté completamente cargada

    download_all_options(driver, output_folder)

    print("Proceso completado.")
finally:
    driver.quit()