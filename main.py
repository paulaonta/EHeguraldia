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

createDirectory("./results")
directory = "./results/pamplonaMAN"
createDirectory(directory)
csv_list = []

partial_link = "http://meteo.navarra.es/_data/datos_estaciones/estacion_196/datos%20diarios/pamplona%20man_"
years = [str(i) for i in range(1880, 2022)] #2022 is not taking into account
i = 0
while i < len(years):
    try:
        # open the link
        link = partial_link + years[i] +".csv"
        # 2. download the data behind the URL
        response = requests.get(link)
        # 3. Open the response into a new file 
        open(directory+"/"+years[i]+".csv", "wb").write(response.content)
        i += 1
        csv_list.append(directory+"/"+years[i]+".csv")
    except:
        print("error: an error occurs while opening the link: "+ link)
        pass
#merge all the csv-s in one
# merging the files
# Return a list of all joined files
combined_csv = pd.concat([pd.read_csv(f, encoding='latin-1') for f in csv_list ])
#to .csv
combined_csv.to_csv(directory+"/pamplonaMAN.csv", index=False, encoding='latin-1')

#convert to json
json_directory = "./results/pamplonaMAN/pamplonaMAN.json"
createFile(json_directory)
convert_toJSON(json_directory, csv_list)