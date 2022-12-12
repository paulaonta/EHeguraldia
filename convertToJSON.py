import csv
import  json

text = {
    "license": "CC0-1.0",
    "description": {
        "eu": "Pamplonako datu meteorologikoak"
    },
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
                "name": "avgLowTemp",
                "type": "number",
                "title": {
                    "eu": "Tenperatura minimoaren batezbestekoa"
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
                "name": "precip",
                "type": "number",
                "title": {
                    "eu": "Prezipitazioak"
                }
            }
        ]
    },
}

def convert_toJSON(directory, files):
    rows = []
    for f in files:
        year = str(f).split(".csv")[0].split("/")[-1]
        # open csv files
        mycsv = csv.reader(open(f, encoding='latin-1'))

        first = True
        max_tenp = -float("Inf")
        min_tenp = float("Inf")
        bb_max = 0.0
        bb_min = 0.0
        bb_prez = 0.0
        cont = 0

        for line in mycsv:
            if first:
                first = False
            else:
                cont += 1
                #get all element in an array
                all_element = "".join(line).split(";") #[0] data, [1] max. temp, [2] min. temp, [3] prez.
                all_element = ['0.0' if elem == '' else elem for elem in all_element]
                if max_tenp < float(all_element[1]):
                    max_tenp = float(all_element[1])
                if min_tenp > float(all_element[2]):
                    min_tenp = float(all_element[2])
                bb_max += float(all_element[1])
                bb_min += float(all_element[2])
                bb_prez += float(all_element[3])
        bb_max /= cont
        bb_min /= cont
        bb_prez /= cont
        rows.append([year, max_tenp, bb_max, bb_min, min_tenp, bb_prez])
    text['data'] = rows

    # Serializing json
    json_object = json.dumps(text, indent=4)
    # Writing to sample.json

    with open(directory, "w") as outfile:
        outfile.write(json_object)
