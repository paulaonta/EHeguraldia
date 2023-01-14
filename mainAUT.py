import os, csv
from urllib.request import urlopen
import bs4
# 1. Import the requests library
import requests
import pandas as pd
import glob
import os
from convertToJSON import *


def createFile(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

def createDirectory(path):
    if not os.path.exists(path):
        os.mkdir(path)

stations = ["ablitas%20mapa","abodi%20(pikatua)%20gn", "adiós%20mapa", "aguilar%20de%20codés%20gn", "aibar%20mapa", "aoiz%20gn", "aralar%20gn",
    "arangoiti%20gn", "arazuri%20intia", "artajona%20mapa", "bardenas%20(barranco)%20intia", "bardenas%20(el%20plano)%20mapa", "bardenas%20(el%20yugo)%20gn",
    "bardenas%20(loma%20negra)%20gn", "bargota%20mapa", "beortegi%20gn", "bera%20(larrategaña)%20gn", "cadreita%20intia", "carcastillo%20(la%20oliva)%20gn",
    "carrascal%20gn", "cascante%20mapa", "corella%20intia", "doneztebe-santesteban%20gn", "el%20perdón%20gn", "eltzaburu%20gn", "erremendia%20(salazar)%20gn",
    "estella%20gn", "etxalar%20(orizkiko%20lepoa)%20gn", "etxarri-aranatz%20gn", "falces%20mapa", "fitero%20mapa", "funes%20intia", "getadar%20gn", "goizueta%20gn",
    "gorramendi%20gn", "iñarbegi%20gn", "irabia%20gn", "isaba-refugio%20belagua%20gn", "lerín%20intia", "los%20arcos%20mapa", "lumbier%20intia", "miranda%20de%20arga%20mapa",
    "murillo%20el%20fruto%20mapa", "olite%20intia", "oskotz%20gn", "pamplona%20(etsia)%20upna", "pamplona%20gn", "san%20adrián%20mapa","san%20martín%20de%20unx%20mapa",
    "sartaguda%20%20intia", "sartaguda%20gn", "sesma%20mapa", "tafalla%20gn","traibuenas%20intia", "trinidad%20de%20iturgoien%20gn", "tudela%20(montes%20del%20cierzo)%20gn",
    "tudela%20(valdetellas)%20mapa", "ujué%20gn", "urbasa%20gn", "villanueva%20de%20yerri%20gn", "yesa%20gn"]#, "ancín%20intia"]

stations_name = ["ablitas mapa","abodi (pikatua) gn", "adiós mapa", "aguilar de codés gn", "aibar mapa", "aoiz gn", "aralar gn",
    "arangoiti gn", "arazuri intia", "artajona mapa", "bardenas (barranco) intia", "bardenas (el plano) mapa", "bardenas (el yugo) gn",
    "bardenas (loma negra) gn", "bargota mapa", "beortegi gn", "bera (larrategaña) gn", "cadreita intia", "carcastillo (la oliva) gn",
    "carrascal gn", "cascante mapa", "corella intia", "doneztebe-santesteban gn", "el perdón gn", "eltzaburu gn", "erremendia (salazar) gn",
    "estella gn", "etxalar (orizkiko lepoa) gn", "etxarri-aranatz gn", "falces mapa", "fitero mapa", "funes intia", "getadar gn", "goizueta gn",
    "gorramendi gn", "iñarbegi gn", "irabia gn", "isaba-refugio belagua gn", "lerín intia", "los arcos mapa", "lumbier intia", "miranda de arga mapa",
    "murillo el fruto mapa", "olite intia", "oskotz gn", "pamplona (etsia) upna", "pamplona gn", "san adrián mapa","san martín de unx mapa",
    "sartaguda  intia", "sartaguda gn", "sesma mapa", "tafalla gn","traibuenas intia", "trinidad de iturgoien gn", "tudela (montes del cierzo) gn",
    "tudela (valdetellas) mapa", "ujué gn", "urbasa gn", "villanueva de yerri gn", "yesa gn"]#, "ancín intia"]

codes =["274", "519", "263", "33", "262", "34", "22", "23", "243", "264", "6", "275", "31", "26", "268", "12", "460", "4", "35", "24", "276", "258", "42", "28","461",
        "249", "7", "517", "8", "269", "273", "259", "246", "499", "25", "497", "32", "502","267", "424", "247", "266", "270", "257", "37", "405", "455", "271", "265","5", "21", "423", "9",
        "242", "29", "36", "272","30", "250", "11", "10"]#, "251"]
#WARNING! To get the last station info. is neccesary to change the years to [2015-2022]

assert (len(stations) == len(codes))

#json for ALL data
json_directory_GLOBAL = "./results1/all_stations_AUT.json"
createFile(json_directory_GLOBAL)

for j in range(len(stations)):
    createDirectory("./results1")
    directory = "./results1/" + stations_name[j]
    createDirectory(directory)
    csv_list = []
    partial_link = "http://meteo.navarra.es/_data/datos_estaciones/estacion_"
    partial_link2 = "/datos%20diarios/"
    years = [str(i) for i in range(1880, 2022)] #2022 is not taking into account
    i = 0
    while i < len(years):
        try:
            # open the link
            if "mapa" in stations[j] and int(years[i]) <= 2018:
                link = partial_link + codes[j] + partial_link2 + stations[j] + "ma_" + years[i] + ".csv"
            else:
                link = partial_link + codes[j] + partial_link2 + stations[j] +"_" + years[i] + ".csv"
            # 2. download the data behind the URL
            response = requests.get(link)
            # 3. Open the response into a new file
            if "  <h2>404: archivo o directorio no encontrado.</h2>" not in str(response.content):
                open(directory+"/"+years[i]+".csv", "wb").write(response.content)
                csv_list.append(directory+"/"+years[i]+".csv")
            i += 1
        except:
            print("error: an error occurs while opening the link: "+ link)
            i += 1
            pass
    if len(csv_list) > 0:
        #merge all the csv-s in one
        # merging the files
        # Return a list of all joined files
        combined_csv = pd.concat([pd.read_csv(f, encoding='latin-1') for f in csv_list ])
        #to .csv
        combined_csv.to_csv(directory + "/" + stations_name[j] + ".csv", index=False, encoding='latin-1')

        #convert to json
        json_directory = directory + "/" + stations_name[j] + ".json"
        createFile(json_directory)
        convert_toJSON_AUT(json_directory, csv_list)
        convert_toJSON_GLOBAL_AUT(json_directory_GLOBAL, csv_list, stations_name[j])