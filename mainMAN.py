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
stations = ["abaurregaina-abaurrea%20alta", "aibar%20man", "aldatz",  "alli-larraun" ,"alloz", "altsasu-alsasua", "amaiur-maya", "amillano", "andosilla", "aoiz%20man",
            "arano", "areso", "aribe", "arizkun", "arróniz", "artaiz", "artieda", "artikutza", "aurizberri-espinal", "azanza", "azpirotz",
            "barásoain", "belate", "belzunce", "bera", "bertiz", "betelu", "buñuel",  "cabanillas", "cábrega", "cadreita%20man",
            "caparroso", "carcastillo%20(la%20oliva)%20man", "cáseda", "central%20arrambide", "corella%20man", "doneztebe-santesteban%20man", "epároz",
            "erro", "esparza%20de%20salazar", "estella%20man", "etxalar", "eugi", "falces%20man", "fitero%20man", "galbarra",
            "genevilla", "goizueta", "goni", "igúzquiza", "ilundáin%20man", "iraizotz", "irotz", "irurita%20(baztan)%20man", "irurtzun",
            "isaba-refugio%20belagua%20man", "javier", "larraona", "leire", "leitza", "lekaroz%20man", "lerga", "lerín%20man", "lesaka", "lesaka-san%20anton",
            "lezáun", "lodosa", "los%20arcos", "luzaide-valcarlos", "miranda", "monreal", "monteagudo", "mugiro", "navascués", "noáin%20man", "olague", "olite%20man",
            "olóriz", "oroz-betelu", "otazu", "pamplona%20man", "puente%20la%20reina", "sartaguda%20man", "sesma%20man", "sunbilla", "tudela%20man",
            "urbasa%20man", "urzainqui", "viana", "yesa%20man", "zalba", "zuazu", "zubiri", "zugarramurdi"]

codes= [ "43", "44", "500", "45", "47", "49", "166", "50", "59", "61", "501", "63", "65", "66", "68", "489", "72", "74", "116",
         "78", "80", "81", "84", "85", "227", "87", "88", "90", "93", "95", "96", "97", "98", "100", "101", "108", "210", "112",
         "114", "115", "117", "120", "121", "124", "125", "126", "128", "129", "130", "136", "138", "141", "142", "427", "144",
         "503", "147", "150", "160", "152", "155", "156", "157", "158", "159", "161", "162", "163", "229", "174", "175", "176",
         "456", "178", "180", "183", "186", "187", "190", "191", "196", "199", "211", "213", "215", "219", "222", "226",
         "231", "236", "237", "238", "239", "240"]

assert (len(stations) == len(codes))
for j in range(len(stations)):
    createDirectory("./results")
    directory = "./results/" + stations[j]
    createDirectory(directory)
    csv_list = []
    partial_link = "http://meteo.navarra.es/_data/datos_estaciones/estacion_"
    partial_link2 = "/datos%20diarios/"
    years = [str(i) for i in range(1880, 2022)] #2022 is not taking into account
    i = 0
    while i < len(years):
        try:
            # open the link
            link = partial_link + codes[j] + partial_link2 + stations[j] + "_" + years[i] + ".csv"
            # 2. download the data behind the URL
            response = requests.get(link)
            # 3. Open the response into a new file
            if "  <h2>404: archivo o directorio no encontrado.</h2>" not in str(response.content):
                open(directory + "/" + years[i] + ".csv", "wb").write(response.content)
                csv_list.append(directory + "/" + years[i] + ".csv")
            i += 1
        except:
            print("error: an error occurs while opening the link: " + link)
            i += 1
            pass
    if len(csv_list) > 0:
        # merge all the csv-s in one
        # merging the files
        # Return a list of all joined files
        combined_csv = pd.concat([pd.read_csv(f, encoding='latin-1') for f in csv_list])
        # to .csv
        combined_csv.to_csv(directory + "/" + stations[j] + ".csv", index=False, encoding='latin-1')

        # convert to json
        json_directory = directory + "/" + stations[j] + ".json"
        createFile(json_directory)
        convert_toJSON(json_directory, csv_list)