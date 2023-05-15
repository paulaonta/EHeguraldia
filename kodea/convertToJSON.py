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
                "name": "avgHighTemp",
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
                "name": "avgLowTemp",
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
            },
            {
                "name": "precipDays",
                "type": "number",
                "title": {
                    "eu": "Euria egin duen egun kopurua"
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
                "name": "avgHighTemp",
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
                "name": "avgLowTemp",
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
            },
            {
                "name": "precipDays",
                "type": "number",
                "title": {
                    "eu": "Euria egin duen egun kopurua"
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

    max_tenp = -float("Inf")
    min_tenp = float("Inf")
    bb_tenp_max = 0.0
    alda_bb_max = False
    bb_tenp_min = 0.0
    alda_bb_min = False
    prez = 0.0
    alda_prez = False
    prezDay = 0
    alda_prezDay = False
    cont = 0

    for f in files:
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))
        first = True

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

                if prev_month != month:
                    bb_tenp_max /= cont
                    bb_tenp_min /= cont
                    if max_tenp == -float("Inf") or not alda_bb_max:
                        max_tenp = 'null'
                    if min_tenp == float("Inf") or not alda_bb_min:
                        min_tenp = 'null'
                    if not alda_bb_max:
                        bb_tenp_max = 'null'
                    if not alda_bb_min:
                        bb_tenp_min = 'null'
                    if not alda_prez:
                        prez = 'null'
                    if not alda_prezDay:
                        prezDay = 'null'

                    if prev_month == "12":
                        rows.append([str(int(year)-1)+"-"+prev_month, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez, prezDay])
                    else:
                        rows.append([year+"-"+prev_month, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez, prezDay])

                    max_tenp = -float("Inf")
                    min_tenp = float("Inf")
                    bb_tenp_max = 0.0
                    alda_bb_max = False
                    bb_tenp_min = 0.0
                    alda_bb_min = False
                    prez = 0.0
                    alda_prez = False
                    prezDay = 0
                    alda_prezDay = False
                    cont = 0

                if len(all_element) == 3:
                    print("it is not complete file: " +str(f))
                    pos_min = 1
                    pos_prez = 2
                else:
                    if max_tenp < float(all_element[pos_max]):
                        max_tenp = float(all_element[pos_max])
                    bb_tenp_max += float(all_element[pos_max])
                    if bb_tenp_max > 0.0:
                        alda_bb_max = True

                if min_tenp > float(all_element[pos_min]):
                    min_tenp = float(all_element[pos_min])
                prez += float(all_element[pos_prez])
                if prez > 0.0:
                    alda_prez = True
                if float(all_element[pos_prez]) > 0.0:
                    prezDay += 1
                    alda_prezDay = True
                bb_tenp_min += float(all_element[pos_min])
                if bb_tenp_min > 0.0:
                    alda_bb_min = True


    bb_tenp_max /= cont
    bb_tenp_min /= cont
    if max_tenp == -float("Inf") or not alda_bb_max:
        max_tenp = 'null'
    if min_tenp == float("Inf") or not alda_bb_min:
        min_tenp = 'null'
    if not alda_bb_max:
        bb_tenp_max = 'null'
    if not alda_bb_min:
        bb_tenp_min = 'null'
    if not alda_prez:
        prez = 'null'
    if not alda_prezDay:
        prezDay = 'null'

    rows.append([year+"-"+prev_month, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez, prezDay])

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
    pos_media = 2
    pos_hez = 4

    max_tenp = -float("Inf")
    min_tenp = float("Inf")
    bb_tenp_max = 0.0
    alda_bb_max = False
    bb_tenp_min = 0.0
    alda_bb_min = False
    prez = 0.0
    alda_prez = False
    prezDay = 0
    alda_prezDay = False
    cont = 0
    cont = 0
    bb = 0.0
    alda_bb = False
    hez = 0.0
    alda_hez = False
    for f in files:
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))

        first = True

        for line in mycsv:
            if first:
                first = False
            else:
                cont += 1
                # get all element in an array
                all_element = "".join(line).split(";")  # [0] data, [1] max. temp, [2] min. temp, [3] prez.
                all_element = ['0.0' if elem == '' else elem for elem in all_element]
                year = all_element[0].split(" ")[0].split("/")[-1]
                if year == "2020":
                    pos_min = 2
                    pos_prez = 5
                else:
                    pos_min = 3
                    pos_prez = 7
                prev_month = month
                month = all_element[0].split(" ")[0].split("/")[1]

                if prev_month != month:
                    bb_tenp_max /= cont
                    bb_tenp_min /= cont
                    bb /= cont
                    hez /= cont
                    if max_tenp == -float("Inf") or not alda_bb_max :
                        max_tenp = 'null'
                    if min_tenp == float("Inf") or not alda_bb_min:
                        min_tenp = 'null'
                    if not alda_bb_max:
                        bb_tenp_max = 'null'
                    if not alda_bb_min:
                        bb_tenp_min = 'null'
                    if not alda_prez:
                        prez = 'null'
                    if not alda_prezDay:
                        prezDay = 'null'
                    if not alda_bb:
                        bb = "null"
                    if not alda_hez:
                        hez = "null"
                    if year == "2020":
                        bb = 'null'
                        hez = 'null'

                    if prev_month == "12":
                        rows.append([str(int(year) - 1)+"-"+prev_month, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez, prezDay])
                    else:
                        rows.append([year+"-"+prev_month, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez, prezDay])

                    max_tenp = -float("Inf")
                    min_tenp = float("Inf")
                    bb_tenp_max = 0.0
                    alda_bb_max = False
                    bb_tenp_min = 0.0
                    alda_bb_min = False
                    prez = 0.0
                    alda_prez = False
                    prezDay = 0
                    alda_prezDay = False
                    cont = 0
                    bb = 0.0
                    alda_bb = False
                    hez = 0.0
                    alda_hez = False

                if max_tenp < float(all_element[pos_max]):
                    max_tenp = float(all_element[pos_max])
                bb_tenp_max += float(all_element[pos_max])
                if bb_tenp_max > 0.0:
                    alda_bb_max = True
                if min_tenp > float(all_element[pos_min]):
                    min_tenp = float(all_element[pos_min])
                prez += float(all_element[pos_prez])
                if prez > 0.0:
                    alda_prez = True
                if float(all_element[pos_prez]) > 0.0:
                    prezDay += 1
                    alda_prezDay = True
                bb_tenp_min += float(all_element[pos_min])
                if bb_tenp_min > 0.0:
                    alda_bb_min = True
                bb += float(all_element[pos_media])
                if bb > 0.0:
                    alda_bb = True
                hez += float(all_element[pos_hez])
                if hez > 0.0:
                    alda_hez = True

    bb_tenp_max /= cont
    bb_tenp_min /= cont
    bb /= cont
    hez /= cont
    if max_tenp == -float("Inf") or not alda_bb_max:
        max_tenp = 'null'
    if min_tenp == float("Inf") or not alda_bb_min:
        min_tenp = 'null'
    if not alda_bb_max:
        bb_tenp_max = 'null'
    if not alda_bb_min:
        bb_tenp_min = 'null'
    if not alda_prez:
        prez = 'null'
    if not alda_prezDay:
        prezDay = 'null'
    if not alda_bb:
        bb = "null"
    if not alda_hez:
        hez = "null"
    if year == "2020":
        bb = 'null'
        hez = 'null'
    rows.append([year+"-"+prev_month, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez, prezDay])
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
    pos_media = 2

    max_tenp = -float("Inf")
    min_tenp = float("Inf")
    bb_tenp_max = 0.0
    alda_bb_max = False
    bb_tenp_min = 0.0
    alda_bb_min = False
    prez = 0.0
    alda_prez = False
    prezDay = 0
    alda_prezDay = False
    cont = 0
    bb = 0.0
    alda_bb = False
    hez = 0.0
    alda_hez = False
    for f in files:
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))

        first = True

        for line in mycsv:
            if first:
                first = False
            else:
                cont += 1
                # get all element in an array
                all_element = "".join(line).split(";")  # [0] data, [1] max. temp, [2] min. temp, [3] prez.
                all_element = ['0.0' if elem == '' else elem for elem in all_element]
                year = all_element[0].split(" ")[0].split("/")[-1]
                if year == "2020":
                    pos_min = 2
                    pos_prez = 5
                    pos_hez = 1
                else:
                    pos_min = 3
                    pos_prez = 7
                    pos_hez = 4

                prev_month = month
                month = all_element[0].split(" ")[0].split("/")[1]

                if prev_month != month:
                    bb_tenp_max /= cont
                    bb_tenp_min /= cont
                    bb /= cont
                    hez /= cont
                    if max_tenp == -float("Inf") or not alda_bb_max:
                        max_tenp = 'null'
                    if min_tenp == float("Inf") or not alda_bb_min:
                        min_tenp = 'null'
                    if not alda_bb_max:
                        bb_tenp_max = 'null'
                    if not alda_bb_min:
                        bb_tenp_min = 'null'
                    if not alda_prez:
                        prez = 'null'
                    if not alda_prezDay:
                        prezDay = 'null'
                    if not alda_bb:
                        bb = "null"
                    if not alda_hez:
                        hez = "null"
                    if year == "2020":
                        bb = 'null'
                        hez = 'null'

                    if prev_month == "12":
                        rows.append(
                            [str(int(year) - 1)+"-"+prev_month, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez, prezDay])
                    else:
                        rows.append([year+"-"+prev_month, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez, prezDay])

                    max_tenp = -float("Inf")
                    min_tenp = float("Inf")
                    bb_tenp_max = 0.0
                    alda_bb_max = False
                    bb_tenp_min = 0.0
                    alda_bb_min = False
                    prez = 0.0
                    alda_prez = False
                    prezDay = 0
                    alda_prezDay = False
                    cont = 0
                    cont = 0
                    bb = 0.0
                    alda_bb = False
                    hez = 0.0
                    alda_hez = False

                if max_tenp < float(all_element[pos_max]):
                    max_tenp = float(all_element[pos_max])
                bb_tenp_max += float(all_element[pos_max])
                if bb_tenp_max>0.0:
                    alda_bb_max = True
                if min_tenp > float(all_element[pos_min]):
                    min_tenp = float(all_element[pos_min])
                prez += float(all_element[pos_prez])
                if prez > 0.0:
                    alda_prez = True
                if float(all_element[pos_prez]) > 0.0:
                    prezDay += 1
                    alda_prezDay = True
                bb_tenp_min += float(all_element[pos_min])
                if bb_tenp_min > 0.0:
                    alda_bb_min = True
                bb += float(all_element[pos_media])
                if bb > 0.0:
                    alda_bb = True
                hez += float(all_element[pos_hez])
                if hez > 0.0:
                    alda_hez = True


    bb_tenp_max /= cont
    bb_tenp_min /= cont
    bb /= cont
    hez /= cont
    if max_tenp == -float("Inf") or not alda_bb_max:
        max_tenp = 'null'
    if min_tenp == float("Inf") or not alda_bb_min:
        min_tenp = 'null'
    if not alda_bb_max:
        bb_tenp_max = 'null'
    if not alda_bb_min:
        bb_tenp_min = 'null'
    if not alda_prez:
        prez = 'null'
    if not alda_prezDay:
        prezDay = 'null'
    if not alda_bb:
        bb = "null"
    if not alda_hez:
        hez = "null"
    if year == "2020":
        bb = 'null'
        hez = 'null'

    rows.append([year+"-"+prev_month, bb, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, hez, prez, prezDay])
    text2['data'] = rows

    # Serializing json
    json_object = json.dumps(text2, indent=4)
    # Writing to sample.json
    first_text = "xxx \n '''Data:" +name +"-AUT.tab''' \n"
    last_text = "\nyyy\nxxx \n'''Data_talk:" + name + "-AUT.tab'''[[Category:Tabular data of weather in Navarre]]\nyyy\n"
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

    max_tenp = -float("Inf")
    min_tenp = float("Inf")
    bb_tenp_max = 0.0
    alda_bb_max = False
    bb_tenp_min = 0.0
    alda_bb_min = False
    prez = 0.0
    alda_prez = False
    prezDay = 0
    alda_prezDay = False
    cont = 0
    for f in files:
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))

        first = True

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

                if prev_month != month:
                    bb_tenp_max /= cont
                    bb_tenp_min /= cont
                    if max_tenp == -float("Inf") or not alda_bb_max :
                        max_tenp = 'null'
                    if min_tenp == float("Inf") or not alda_bb_min:
                        min_tenp = 'null'
                    if not alda_bb_max:
                        bb_tenp_max = 'null'
                    if not alda_bb_min:
                        bb_tenp_min = 'null'
                    if not alda_prez:
                        prez = 'null'
                    if not alda_prezDay:
                        prezDay = 'null'
                    if prev_month == "12":
                        rows.append([str(int(year)-1)+"-"+prev_month, max_tenp, bb_tenp_max, min_tenp,bb_tenp_min, prez, prezDay])
                    else:
                        rows.append([year+"-"+prev_month, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez, prezDay])

                    max_tenp = -float("Inf")
                    min_tenp = float("Inf")
                    bb_tenp_max = 0.0
                    alda_bb_max = False
                    bb_tenp_min = 0.0
                    alda_bb_min = False
                    prez = 0.0
                    alda_prez = False
                    prezDay = 0
                    alda_prezDay = False
                    cont = 0

                if len(all_element) == 3:
                    print("it is not complete file: " +str(f))
                    pos_min = 1
                    pos_prez = 2
                else:
                    if max_tenp < float(all_element[pos_max]):
                        max_tenp = float(all_element[pos_max])
                    bb_tenp_max += float(all_element[pos_max])
                    if bb_tenp_max > 0.0:
                        alda_bb_max = True

                if min_tenp > float(all_element[pos_min]):
                    min_tenp = float(all_element[pos_min])
                prez += float(all_element[pos_prez])
                if prez > 0.0:
                    alda_prez = True
                if float(all_element[pos_prez]) > 0.0:
                    prezDay += 1
                    alda_prezDay = True
                bb_tenp_min += float(all_element[pos_min])
                if bb_tenp_min > 0.0:
                    alda_bb_min = True


    bb_tenp_max /= cont
    bb_tenp_min /= cont
    if max_tenp == -float("Inf") or not alda_bb_max:
        max_tenp = 'null'
    if min_tenp == float("Inf") or not alda_bb_min:
        min_tenp = 'null'
    if not alda_bb_max:
        bb_tenp_max = 'null'
    if not alda_bb_min:
        bb_tenp_min = 'null'
    if not alda_prez:
        prez = 'null'
    if not alda_prezDay:
        prezDay = 'null'

    rows.append([year+"-"+prev_month, max_tenp, bb_tenp_max, min_tenp, bb_tenp_min, prez, prezDay])

    text['data'] = rows

    # Serializing json
    json_object = json.dumps(text, indent=4)

    # Writing to sample.json
    first_text = "xxx \n '''Data:" + name + "-MAN.tab''' \n"
    last_text = "\nyyy\nxxx \n'''Data_talk:" + name + "-MAN.tab'''[[Category:Tabular data of weather in Navarre]]\nyyy\n"
    with open(directory, "a") as outfile:
        outfile.write(first_text)
        outfile.write(json_object)
        outfile.write(last_text)
