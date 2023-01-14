import csv
import  json


text = {
    "license": "CC0-1.0",
    "description": { "eu":"Datu meteorologikoak"},
    "schema": {
        "fields": [
            {
                "name": "date",
                "type": "string",
                "title": {
                    "ar": "data"
                }
            },
            {
                "name": "highTemp",
                "type": "number",
                "title": {
                    "eu": "Tenperatura maximoa"
                }
            },
{
                "name": "highTempAvg",
                "type": "number",
                "title": {
                    "eu": "Tenperatura maximoaren batezbestekoa"
                }
            },
            {
                "name": "lowTemp",
                "type": "number",
                "title": {
                    "eu": "Tenperatura minimoa"
                }
            },
{
                "name": "lowTempAvg",
                "type": "number",
                "title": {
                    "eu": "Tenperatura minimoaren batezbestekoa"
                }
            },
            {
                "name": "precip",
                "type": "number",
                "title": {
                    "eu": "Pilatutako prezipitazioak"
                }
            }
        ]
    },
}

text2 = {
    "license": "CC0-1.0",
    "description": { "eu":"Datu meteorologikoak"},
    "schema": {
        "fields": [
            {
                "name": "date",
                "type": "string",
                "title": {
                    "ar": "data"
                }
            },
            {
                "name": "avgTemp",
                "type": "number",
                "title": {
                    "eu": "Batazbesteko tenperatura"
                }
            },
            {
                "name": "highTemp",
                "type": "number",
                "title": {
                    "eu": "Tenperatura maximoa"
                }
            },
{
                "name": "highTempAvg",
                "type": "number",
                "title": {
                    "eu": "Tenperatura maximoaren batezbestekoa"
                }
            },
            {
                "name": "lowTemp",
                "type": "number",
                "title": {
                    "eu": "Tenperatura minimoa"
                }
            },
{
                "name": "lowTempAvg",
                "type": "number",
                "title": {
                    "eu": "Tenperatura minimoaren batezbestekoa"
                }
            },
            {
                "name": "hez",
                "type": "number",
                "title": {
                    "eu": "Batazbesteko hezetasuna"
                }
            },
            {
                "name": "precip",
                "type": "number",
                "title": {
                    "eu": "Pilatutako prezipitazioak"
                }
            }
        ]
    },
}

def convert_toJSON(directory, files):
    rows = []
    month = "01"
    pos_max = 1
    pos_min = 2
    pos_prez = 3
    for f in files:
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))

        first = True
        max_tenp = -float("Inf")
        min_tenp = float("Inf")
        bb_tenp_max = 0.0
        bb_tenp_min = 0.0
        prez = 0.0
        cont = 0

        for line in mycsv:
            if first:
                first = False
            else:
                cont += 1
                #get all element in an array
                all_element = "".join(line).split(";") #[0] data, [1] max. temp, [2] min. temp, [3] prez.
                all_element = ['0.0' if elem == '' else elem for elem in all_element]
                year = all_element[0].split(" ")[0].split("/")[-1]
                prev_month = month
                month = all_element[0].split(" ")[0].split("/")[1]

                if len(all_element) == 3:
                    print("it is not complete file: " +str(f))
                    pos_min = 1
                    pos_prez = 2
                else:
                    if max_tenp < float(all_element[pos_max]):
                        max_tenp = float(all_element[pos_max])
                    bb_tenp_max += float(all_element[pos_max])

                if min_tenp > float(all_element[pos_min]):
                    min_tenp = float(all_element[pos_min])
                prez += float(all_element[pos_prez])
                bb_tenp_min += float(all_element[pos_min])

                if prev_month != month:
                    bb_tenp_max /= cont
                    bb_tenp_min /= cont
                    prez /= cont
                    if max_tenp == 0.0:
                        max_tenp = 'null'
                    if min_tenp == 0.0:
                        min_tenp = 'null'
                    if bb_tenp_max == 0.0:
                        bb_tenp_max = 'null'
                    if bb_tenp_min == 0.0:
                        bb_tenp_min = 'null'
                    if prez == 0.0:
                        prez = 'null'

                    if prev_month == "12":
                        rows.append([prev_month + "/" + str(int(year)-1), max_tenp, bb_tenp_max, min_tenp,bb_tenp_min, prez])
                    else:
                        rows.append([prev_month + "/" + year, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez])

                    max_tenp = -float("Inf")
                    min_tenp = float("Inf")
                    bb_tenp_max = 0.0
                    bb_tenp_min = 0.0
                    prez = 0.0
                    cont = 0
    bb_tenp_max /= cont
    bb_tenp_min /= cont
    prez /= cont
    if max_tenp == 0.0:
        max_tenp = 'null'
    if min_tenp == 0.0:
        min_tenp = 'null'
    if bb_tenp_max == 0.0:
        bb_tenp_max = 'null'
    if bb_tenp_min == 0.0:
        bb_tenp_min = 'null'
    if prez == 0.0:
        prez = 'null'

    rows.append([prev_month + "/" + year, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez])

    text['data'] = rows

    # Serializing json
    json_object = json.dumps(text, indent=4)
    # Writing to sample.json

    with open(directory, "w") as outfile:
        outfile.write(json_object)


def convert_toJSON_AUT(directory, files):
    rows = []
    month = "01"
    pos_max = 1
    pos_min = 2
    pos_prez = 5
    pos_media = 3
    pos_hez = 4
    for f in files:
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))

        first = True
        max_tenp = -float("Inf")
        min_tenp = float("Inf")
        bb_tenp_max = 0.0
        bb_tenp_min = 0.0
        prez = 0.0
        cont = 0
        bb = 0.0
        hez = 0.0

        for line in mycsv:
            if first:
                first = False
            else:
                cont += 1
                # get all element in an array
                all_element = "".join(line).split(";")  # [0] data, [1] max. temp, [2] min. temp, [3] prez.
                all_element = ['0.0' if elem == '' else elem for elem in all_element]
                year = all_element[0].split(" ")[0].split("/")[-1]
                prev_month = month
                month = all_element[0].split(" ")[0].split("/")[1]


                if max_tenp < float(all_element[pos_max]):
                    max_tenp = float(all_element[pos_max])
                bb_tenp_max += float(all_element[pos_max])
                if min_tenp > float(all_element[pos_min]):
                    min_tenp = float(all_element[pos_min])
                prez += float(all_element[pos_prez])
                bb_tenp_min += float(all_element[pos_min])
                bb += float(all_element[pos_media])
                hez += float(all_element[pos_hez])

                if prev_month != month:
                    bb_tenp_max /= cont
                    bb_tenp_min /= cont
                    bb /= cont
                    prez /= cont
                    hez /= cont
                    if max_tenp == 0.0:
                        max_tenp = 'null'
                    if min_tenp == 0.0:
                        min_tenp = 'null'
                    if bb_tenp_max == 0.0:
                        bb_tenp_max = 'null'
                    if bb_tenp_min == 0.0:
                        bb_tenp_min = 'null'
                    if prez == 0.0:
                        prez = 'null'
                    if bb == 0.0:
                        bb = 'null'
                    if hez == 0.0:
                        hez = 'null'

                    if prev_month == "12":
                        rows.append(
                            [prev_month + "/" + str(int(year) - 1), bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez])
                    else:
                        rows.append([prev_month + "/" + year, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez])

                    max_tenp = -float("Inf")
                    min_tenp = float("Inf")
                    bb = 0.0
                    bb_tenp_max = 0.0
                    bb_tenp_min = 0.0
                    prez = 0.0
                    hez = 0.0
                    cont = 0
    bb_tenp_max /= cont
    bb_tenp_min /= cont
    bb /= cont
    prez /= cont
    hez /= cont
    if max_tenp == 0.0:
        max_tenp = 'null'
    if min_tenp == 0.0:
        min_tenp = 'null'
    if bb_tenp_max == 0.0:
        bb_tenp_max = 'null'
    if bb_tenp_min == 0.0:
        bb_tenp_min = 'null'
    if prez == 0.0:
        prez = 'null'
    if bb == 0.0:
        bb = 'null'
    if hez == 0.0:
        hez = 'null'

    rows.append([prev_month + "/" + year, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez])
    text2['data'] = rows

    # Serializing json
    json_object = json.dumps(text2, indent=4)
    # Writing to sample.json

    with open(directory, "w") as outfile:
        outfile.write(json_object)


def convert_toJSON_GLOBAL_AUT(directory, files, name):
    rows = []
    month = "01"
    pos_max = 1
    pos_min = 2
    pos_prez = 5
    pos_media = 3
    pos_hez = 4
    for f in files:
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))

        first = True
        max_tenp = -float("Inf")
        min_tenp = float("Inf")
        bb_tenp_max = 0.0
        bb_tenp_min = 0.0
        prez = 0.0
        cont = 0
        bb = 0.0
        hez = 0.0

        for line in mycsv:
            if first:
                first = False
            else:
                cont += 1
                # get all element in an array
                all_element = "".join(line).split(";")  # [0] data, [1] max. temp, [2] min. temp, [3] prez.
                all_element = ['0.0' if elem == '' else elem for elem in all_element]
                year = all_element[0].split(" ")[0].split("/")[-1]
                prev_month = month
                month = all_element[0].split(" ")[0].split("/")[1]


                if max_tenp < float(all_element[pos_max]):
                    max_tenp = float(all_element[pos_max])
                bb_tenp_max += float(all_element[pos_max])
                if min_tenp > float(all_element[pos_min]):
                    min_tenp = float(all_element[pos_min])
                prez += float(all_element[pos_prez])
                bb_tenp_min += float(all_element[pos_min])
                bb += float(all_element[pos_media])
                hez += float(all_element[pos_hez])

                if prev_month != month:
                    bb_tenp_max /= cont
                    bb_tenp_min /= cont
                    bb /= cont
                    prez /= cont
                    hez /= cont
                    if max_tenp == 0.0:
                        max_tenp = 'null'
                    if min_tenp == 0.0:
                        min_tenp = 'null'
                    if bb_tenp_max == 0.0:
                        bb_tenp_max = 'null'
                    if bb_tenp_min == 0.0:
                        bb_tenp_min = 'null'
                    if prez == 0.0:
                        prez = 'null'
                    if bb == 0.0:
                        bb = 'null'
                    if hez == 0.0:
                        hez = 'null'

                    if prev_month == "12":
                        rows.append(
                            [prev_month + "/" + str(int(year) - 1), bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez])
                    else:
                        rows.append([prev_month + "/" + year, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez])

                    max_tenp = -float("Inf")
                    min_tenp = float("Inf")
                    bb = 0.0
                    bb_tenp_max = 0.0
                    bb_tenp_min = 0.0
                    prez = 0.0
                    hez = 0.0
                    cont = 0
    bb_tenp_max /= cont
    bb_tenp_min /= cont
    bb /= cont
    prez /= cont
    hez /= cont
    if max_tenp == 0.0:
        max_tenp = 'null'
    if min_tenp == 0.0:
        min_tenp = 'null'
    if bb_tenp_max == 0.0:
        bb_tenp_max = 'null'
    if bb_tenp_min == 0.0:
        bb_tenp_min = 'null'
    if prez == 0.0:
        prez = 'null'
    if bb == 0.0:
        bb = 'null'
    if hez == 0.0:
        hez = 'null'

    rows.append([prev_month + "/" + year, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez])
    text2['data'] = rows

    # Serializing json
    json_object = json.dumps(text2, indent=4)
    # Writing to sample.json
    first_text = "xxx \n '''Data:" +name +"-AUT.tab''' \n"
    last_text = "\nyyy\nxxx \n'''Data_talk:" + name + "-AUT.tab'''[[Category:Weather tabs of towns in Nafarroa]]\nyyy\n"
    with open(directory, "a") as outfile:
        outfile.write(first_text)
        outfile.write(json_object)
        outfile.write(last_text)

def convert_toJSON_GLOBAL(directory, files, name):
    rows = []
    month = "01"
    pos_max = 1
    pos_min = 2
    pos_prez = 3
    for f in files:
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))

        first = True
        max_tenp = -float("Inf")
        min_tenp = float("Inf")
        bb_tenp_max = 0.0
        bb_tenp_min = 0.0
        prez = 0.0
        cont = 0

        for line in mycsv:
            if first:
                first = False
            else:
                cont += 1
                #get all element in an array
                all_element = "".join(line).split(";") #[0] data, [1] max. temp, [2] min. temp, [3] prez.
                all_element = ['0.0' if elem == '' else elem for elem in all_element]
                year = all_element[0].split(" ")[0].split("/")[-1]
                prev_month = month
                month = all_element[0].split(" ")[0].split("/")[1]

                if len(all_element) == 3:
                    print("it is not complete file: " +str(f))
                    pos_min = 1
                    pos_prez = 2
                else:
                    if max_tenp < float(all_element[pos_max]):
                        max_tenp = float(all_element[pos_max])
                    bb_tenp_max += float(all_element[pos_max])

                if min_tenp > float(all_element[pos_min]):
                    min_tenp = float(all_element[pos_min])
                prez += float(all_element[pos_prez])
                bb_tenp_min += float(all_element[pos_min])

                if prev_month != month:
                    bb_tenp_max /= cont
                    bb_tenp_min /= cont
                    prez /= cont
                    if max_tenp == 0.0:
                        max_tenp = 'null'
                    if min_tenp == 0.0:
                        min_tenp = 'null'
                    if bb_tenp_max == 0.0:
                        bb_tenp_max = 'null'
                    if bb_tenp_min == 0.0:
                        bb_tenp_min = 'null'
                    if prez == 0.0:
                        prez = 'null'

                    if prev_month == "12":
                        rows.append([prev_month + "/" + str(int(year)-1), max_tenp, bb_tenp_max, min_tenp,bb_tenp_min, prez])
                    else:
                        rows.append([prev_month + "/" + year, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez])

                    max_tenp = -float("Inf")
                    min_tenp = float("Inf")
                    bb_tenp_max = 0.0
                    bb_tenp_min = 0.0
                    prez = 0.0
                    cont = 0
    bb_tenp_max /= cont
    bb_tenp_min /= cont
    prez /= cont
    if max_tenp == 0.0:
        max_tenp = 'null'
    if min_tenp == 0.0:
        min_tenp = 'null'
    if bb_tenp_max == 0.0:
        bb_tenp_max = 'null'
    if bb_tenp_min == 0.0:
        bb_tenp_min = 'null'
    if prez == 0.0:
        prez = 'null'

    rows.append([prev_month + "/" + year, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez])

    text['data'] = rows

    # Serializing json
    json_object = json.dumps(text, indent=4)

    # Writing to sample.json
    first_text = "xxx \n '''Data:" + name + "-MAN.tab''' \n"
    last_text = "\nyyy\nxxx \n'''Data_talk:" + name + "-MAN.tab'''[[Category:Weather tabs of towns in Nafarroa]]\nyyy\n"
    with open(directory, "a") as outfile:
        outfile.write(first_text)
        outfile.write(json_object)
        outfile.write(last_text)
