# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 16:47:48 2020

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
temp_folder_path = r'D:\mini-trabajos\ONPE-Scrap\temp14'    
output_folder_path = r'D:\mini-trabajos\ONPE-Scrap\Output14'
driver_path = r'D:\mini-trabajos\SIAF Innovacion\Code\Chromedriver\chromedriver.exe'


new_dir = os.path.join( temp_folder_path, r"Donwloads_distrital" )
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
driver.get(r"https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2014/PRERM2014/Resultados-Ubigeo-Provincial-EM.html")
#### Obtener datos de los deparmentos
list_cantidad_dist=[]
List_votos=[]
List_participacion = []
sub_sector = None
time.sleep(1)
while not sub_sector:
    content=driver.page_source             #### Se descarga el codigo HTML
    soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
    try:
        sub_sector = soup.find_all(id='departamentos')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
    except NoSuchElementException:
        time.sleep(0.3)        
sub_sector1 = sub_sector[0].find_all('option')        ### Se busca los input para seleccionar 
list_sub_sector1=[]
list_names_dept = []
for dept_sub in sub_sector1:
    a = dept_sub.get('value')
    b = dept_sub.text
    list_names_dept.append(b)
    list_sub_sector1.append(a)
list_sub_sector1.remove('')  
list_names_dept.remove('--SELECCIONE--')  


for dept in list_sub_sector1[3:]:  
    numdpt = list_sub_sector1.index(dept)
    print(dept)
    name_dpt = list_names_dept[numdpt]
    time.sleep(1)
    next_enable=None ### Define a logic variabl
    while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found.
        try:
            click_enable = driver.find_element_by_xpath("//*[@id='cdgoDep']/option[@value='%s']" %dept)  ### Definition of element that will be sought
            next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
        except NoSuchElementException:
            time.sleep(0.3)
    click_enable.click()
    time.sleep(5)  
    
    provincias = None
    while not provincias:
        content=driver.page_source             #### Se descarga el codigo HTML
        soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
        try:
            provincias = soup.find_all(id='provincias')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
        except NoSuchElementException:
            time.sleep(0.3)        
    sub_provincias = provincias[0].find_all('option')  
    
    list_names_prov=[]
    list_sub_provincias=[]
    for prov_sub in sub_provincias:
        a= prov_sub.get('value')
        b= prov_sub.text
        list_names_prov.append(b)
        list_sub_provincias.append(a)
    list_sub_provincias.remove('')
    list_names_prov.remove('--SELECCIONE--')
    

    for provin in list_sub_provincias:  
        print("         " + provin)
        numprov = list_sub_provincias.index(provin)
        numprovi = list_names_prov[numprov]
        time.sleep(1)
        next_enable=None ### Define a logic variabl
        while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found.
            try:
                click_enable = driver.find_element_by_xpath("//*[@id='cdgoProv']/option[@value='%s']" %provin)  ### Definition of element that will be sought
                next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
            except NoSuchElementException:
                time.sleep(0.3)
        click_enable.click()
        time.sleep(5)

        list_sub_distritos = None
        while not list_sub_distritos:
            content=driver.page_source             #### Se descarga el codigo HTML
            soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
            try:
                distritos = soup.find_all(id='distritos')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
                sub_distritos = distritos[0].find_all('option')
                list_sub_distritos=[]
                list_names_dist = []
                for dist_sub in sub_distritos:
                    a = dist_sub.get('value')
                    b = dist_sub.text
                    list_names_dist.append(b)
                    list_sub_distritos.append(a)
                list_sub_distritos.remove('')        
                list_names_dist.remove(' TODOS ')
            except NoSuchElementException:
                time.sleep(0.3)        
        
        for distr in list_sub_distritos:  
            numdist = list_sub_distritos.index(distr)
            numdistr = list_names_dist[numdist]
            
            print("         " + "         " +  distr)
            time.sleep(1)
            next_enable=None ### Define a logic variabl
            while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found.
                try:
                    click_enable = driver.find_element_by_xpath("//*[@id='cdgoDist']/option[@value='%s']" %distr)  ### Definition of element that will be sought
                    next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                except NoSuchElementException:
                    time.sleep(0.3)
            click_enable.click()
            time.sleep(0.8)
            list_cantidad_dist.append(distr)
            VOTOS = None
            while not VOTOS:
                content=driver.page_source             #### Se descarga el codigo HTML
                soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
                try:
                    VOTOS = soup.find_all(id='resulUbigeo_table')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
                    PART = soup.find_all('div', class_="contenedor-icourna")
                    
                except NoSuchElementException:
                    time.sleep(0.1)        
            tabla_votos     = VOTOS[0]  
            participacion   = PART[0].find_all('label')
            
            participacion_df = pd.DataFrame([participacion[1].text, participacion[3].text]).transpose()
            participacion_df.columns = [participacion[0].text, participacion[2].text]
            participacion_df["Departamento"] = name_dpt
            participacion_df["Provincia"] = numprovi
            participacion_df["Distrito"] = numdistr
            List_participacion.append(participacion_df)
            
            output_rows=[]
            for table_row in tabla_votos.findAll('tr'):
                columns = table_row.findAll('td')
                output_row=[]
                for column in columns:
                    output_row.append(column.text)
                output_rows.append(output_row)
                
            votos_df= pd.DataFrame(output_rows[2: len(output_rows)-4 ])
            del votos_df[0]
            votos_df.columns = [ "organizacion politica", "total votos", "porcentaje votos validos", "porcentaje votos emitidos" ]
            votos_result = pd.DataFrame(output_rows[len(output_rows)-4: ])
            votos_result.columns = [ "organizacion politica", "total votos", "porcentaje votos validos", "porcentaje votos emitidos" ]
            votos_df = pd.concat( [votos_df, votos_result] )
            votos_df["Departamento"]= name_dpt
            votos_df["Provincia"]   = numprovi
            votos_df["Distrito"]    = numdistr            
            List_votos.append(votos_df)
            
len(list_cantidad_dist)           
##### Hasta 40000         
list_votos_4= List_votos            
list_participacion_4= List_participacion            

list_votos_f = list_votos_4 + List_votos
list_part_f = list_participacion_4 +  List_participacion                  
    
for xx in range(0, len(list_votos_f)) :
    if xx==0:
        votos_total = list_votos_f[xx]
    else:
        votos_total = pd.concat( [ votos_total, list_votos_f[xx] ] )

for xx in range(0, len(list_part_f)) :
    if xx==0:
        participa_total = list_part_f[xx]
    else:
        participa_total = pd.concat( [ participa_total, list_part_f[xx] ] )
 

       
votos_total = votos_total.reset_index()     
del votos_total['index']      
Final_file_path = os.path.join(output_folder_path, 'votos_provincia_14.dta')             
votos_total.to_stata(Final_file_path, version=117)

participa_total = participa_total.reset_index()     
del participa_total['index']      
Final_file_path = os.path.join(output_folder_path, 'participacion_provincia_14.dta')             
participa_total.to_stata(Final_file_path, version=117)


            
            
