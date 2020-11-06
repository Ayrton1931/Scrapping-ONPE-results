# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 07:22:17 2020

@author: Shadow
"""

###Packages:
import csv
import re
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.parse as urlparse
import re
def newMatrix(f,c,n):
    matriz=[]
    for i in range(f):
        a=[n]*c
        matriz.append(a)
    return matriz

###### Define Folder path
temp_folder_path = r'D:\mini-trabajos\ONPE-Scrap\temp'    
output_folder_path = r'D:\mini-trabajos\ONPE-Scrap\Output'
driver_path = r'D:\mini-trabajos\SIAF Innovacion\Code\Chromedriver\chromedriver.exe'


new_dir = os.path.join( temp_folder_path, r"Donwloads_provincia" )
if not os.path.exists(new_dir):
    os.makedirs(new_dir)
        
option = webdriver.ChromeOptions() 
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
#option.add_argument("--headless") 
option.add_experimental_option("prefs",  {'download.default_directory' : new_dir,
                                              "safebrowsing.enabled": "false"} )
driver = webdriver.Chrome(options=option, executable_path=driver_path)
driver.get(r"http://resultadoshistorico.onpe.gob.pe/PRERM2018/EleccionesMunicipales/RePro")
list_cantidad_dist=[]
sub_sector = None
while not sub_sector:
    content=driver.page_source             #### Se descarga el codigo HTML
    soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
    try:
        sub_sector = soup.find_all(id='select_departamento')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
    except NoSuchElementException:
        time.sleep(0.1)        
sub_sector1 = sub_sector[0].find_all('option')        ### Se busca los input para seleccionar 
list_sub_sector1=[]
for dept_sub in sub_sector1:
    a= dept_sub.get('value')
    list_sub_sector1.append(a)
for dept in list_sub_sector1:  
    print(dept)
    next_enable=None ### Define a logic variabl
    while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found.
        try:
            click_enable = driver.find_element_by_xpath("//*[@id='select_departamento']/option[@value='%s']" %dept)  ### Definition of element that will be sought
            next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
        except NoSuchElementException:
            time.sleep(0.1)
    click_enable.click()
    time.sleep(0.8)   
    sub_sector_prov = None
    while not sub_sector_prov:
        content=driver.page_source             #### Se descarga el codigo HTML
        soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
        try:
            sub_sector_prov = soup.find_all(attrs= {'name':'cod_prov'})   ### Se busca la parte de code que contiene los input para escoger los pliegos.
        except NoSuchElementException:
            time.sleep(0.1)        
    sub_sector_prov1 = sub_sector_prov[0].find_all('option')        ### Se busca los input para seleccionar 
    list_sub_sector_prov1=[]
    for prov_sub in sub_sector_prov1:
        a= prov_sub.get('value')
        list_sub_sector_prov1.append(a)    
    for prov in list_sub_sector_prov1:
        print("      " + prov  )
        next_enable=None ### Define a logic variabl
        while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found.
            try:
                click_enable = driver.find_element_by_xpath("//*[@name='cod_prov']/option[@value='%s']" %prov)  ### Definition of element that will be sought
                next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
            except NoSuchElementException:
                time.sleep(0.1)
        click_enable.click() 
        time.sleep(0.8)
        sub_sector_dist = None
        while not sub_sector_dist:        
            content=driver.page_source
            soup = BeautifulSoup(content)
            try:
                sub_sector_dist = soup.find_all(attrs= {'name':'cod_dist'})   ### Se busca la parte de code que contiene los input para escoger los pliegos.
            except NoSuchElementException:
                time.sleep(0.1)        
        sub_sector_dist1 = sub_sector_dist[0].find_all('option')        ### Se busca los input para seleccionar 
        list_sub_sector_dist1=[]
        for dist_sub in sub_sector_dist1:
            a= dist_sub.get('value')
            list_sub_sector_dist1.append(a)
        if "0" in list_sub_sector_dist1:
            list_sub_sector_dist1.remove('0')
            
        for dist in list_sub_sector_dist1:
            print("             " + dist  )
            next_enable=None ### Define a logic variabl
            while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found.
                try:
                    click_enable = driver.find_element_by_xpath("//*[@id='cod_dist']/option[@value='%s']" %dist)  ### Definition of element that will be sought
                    next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                except NoSuchElementException:
                    time.sleep(0.1)
            click_enable.click()
            time.sleep(0.8)
            list_cantidad_dist.append(dist)
            next_enable=None                     ### Define a logic variable
            while not next_enable:
                try:
                    click_enable = driver.find_element_by_xpath("//div[@class='icon-excel']")  ### Definition of element that will be sought
                    next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                except NoSuchElementException:
                    time.sleep(0.3)
            click_enable.click()       ### Click the button.             
            time.sleep(0.8)
    
len(list_cantidad_dist)    
    
##############################################################################
############################################################################## Upload Scrap Output
##############################################################################
#### Distritos 
new_dir = os.path.join( temp_folder_path, r"Donwloads_distrital" )
list_of_names_files = os.listdir(new_dir)                #### Obtener los nombres de los archivos de cada carpeta.
for ss in list_of_names_files:
    if re.search( 'desktop.ini', ss ):
        list_of_names_files.remove('desktop.ini') 

List_votos = []
List_participacion = []                                      ### Lista vacia donde se guardaran los archivos descagados.             
for ii in list_of_names_files:
    file_path=os.path.join(new_dir, ii)                         ### Definir la direccion de cada file.
    list_csv=[]
    with open(file_path, newline='', encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ')   
        for row in spamreader:
            list_csv.append(''.join(row)) 
            
            
    Locacion = list_csv[2].split(" >")
    Votos=[]
    names_votos=[]
    for j in range(10, (len(list_csv)-25) ):
        row = re.findall('"([^"]*)"', list_csv[j])
        Votos.append(row)
        names_row = list_csv[j].split(",")[0]
        names_votos.append(names_row)        
    names_votos = pd.DataFrame(names_votos)    
    Votos = pd.DataFrame(Votos)
    Votos = pd.concat( [names_votos, Votos], axis=1 )
    names = list_csv[9].split(",")
    Votos.columns = ['organizacion politica', 'Total', 'porcentaje votos validos','porcentaje votos emitidos']
    Votos["departamento"]=Locacion[0]
    Votos["provincia"]=Locacion[1]
    Votos["distrito"]=Locacion[2]
    List_votos.append(Votos)
    bar = re.findall('"([^"]*)"', list_csv[6])
    bar2='","'.join(bar)
    first = list_csv[6].replace(bar2, "")
    first = first.replace(',""', '') 
    bar.insert(0, first)    
    bar = pd.DataFrame(bar).transpose()
    bar.columns = ["electores habiles", "participacion ciudadana", "porcentaje participacion ciudadana", "actas procesadas"]
    bar["Departamento"]=Locacion[0]
    bar["Provincia"]=Locacion[1]
    bar["Distrito"]=Locacion[2]
    List_participacion.append(bar)    
        
    
for i in range(0, len(List_participacion)):
    if i==0:
        participaciondf = List_participacion[0]
    else:
        participaciondf = pd.concat( [participaciondf, List_participacion[i] ] )

for i in range(0, len(List_votos)):
    if i==0:
        votosdf = List_votos[0]
    else:
        votosdf = pd.concat( [votosdf, List_votos[i] ] )
    
# Exportar los votos a DTA        
votosdf = votosdf.reset_index()     
del votosdf['index']      
Final_file_path = os.path.join(output_folder_path, 'votos_distrito.dta')             
votosdf.to_stata(Final_file_path, version=117) 

# Exportar la participacion a DTA        
participaciondf =participaciondf.reset_index()     
del participaciondf['index']      
Final_file_path = os.path.join(output_folder_path, 'participacion_distrito.dta')             
participaciondf.to_stata(Final_file_path, version=117) 




####################
#################### Provincias
new_dir = os.path.join( temp_folder_path, r"Donwloads_provincia" )
list_of_names_files = os.listdir(new_dir)                #### Obtener los nombres de los archivos de cada carpeta.
for ss in list_of_names_files:
    if re.search( 'desktop.ini', ss ):
        list_of_names_files.remove('desktop.ini') 

List_votos = []
List_participacion = []                                      ### Lista vacia donde se guardaran los archivos descagados.             
for ii in list_of_names_files:
    file_path=os.path.join(new_dir, ii)                         ### Definir la direccion de cada file.
    list_csv=[]
    with open(file_path, newline='', encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ')   
        for row in spamreader:
            list_csv.append(''.join(row)) 
            
            
    Locacion = list_csv[2].split(" >")
    Votos=[]
    names_votos=[]
    for j in range(10, (len(list_csv)-25) ):
        row = re.findall('"([^"]*)"', list_csv[j])
        Votos.append(row)
        names_row = list_csv[j].split(",")[0]
        names_votos.append(names_row)        
    names_votos = pd.DataFrame(names_votos)    
    Votos = pd.DataFrame(Votos)
    Votos = pd.concat( [names_votos, Votos], axis=1 )
    names = list_csv[9].split(",")
    Votos.columns = ['organizacion politica', 'Total', 'porcentaje votos validos','porcentaje votos emitidos']
    Votos["departamento"]=Locacion[0]
    Votos["provincia"]=Locacion[1]
    Votos["distrito"]=Locacion[2]
    List_votos.append(Votos)
    bar = re.findall('"([^"]*)"', list_csv[6])
    bar2='","'.join(bar)
    first = list_csv[6].replace(bar2, "")
    first = first.replace(',""', '') 
    bar.insert(0, first)    
    bar = pd.DataFrame(bar).transpose()
    bar.columns = ["electores habiles", "participacion ciudadana", "porcentaje participacion ciudadana", "actas procesadas"]
    bar["Departamento"]=Locacion[0]
    bar["Provincia"]=Locacion[1]
    bar["Distrito"]=Locacion[2]
    List_participacion.append(bar)    
        
    
for i in range(0, len(List_participacion)):
    if i==0:
        participaciondf = List_participacion[0]
    else:
        participaciondf = pd.concat( [participaciondf, List_participacion[i] ] )

for i in range(0, len(List_votos)):
    if i==0:
        votosdf = List_votos[0]
    else:
        votosdf = pd.concat( [votosdf, List_votos[i] ] )
    
# Exportar votos a DTA        
votosdf = votosdf.reset_index()     
del votosdf['index']      
Final_file_path = os.path.join(output_folder_path, 'votos_provincia.dta')             
votosdf.to_stata(Final_file_path, version=117)


# Exportar participacion a DTA        
participaciondf = participaciondf.reset_index()     
del participaciondf['index']      
Final_file_path = os.path.join(output_folder_path, 'participacion_provincia.dta')             
participaciondf.to_stata(Final_file_path, version=117)
