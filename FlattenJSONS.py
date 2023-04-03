import json
import os
import csv
import sys

def flatten_json(x: dict) -> dict:
    output = []

    def flatten(element, name=''):
        if type(element) is dict:
            if not element:
                output[name[:-1]] = {}
            for key in element:
                flatten(element[key], name + key + '_')
        elif type(element) is list:
            if not element:
                output[name[:-1]] = []
            i = 0
            for k in element:
                flatten(k, name + str(i) + '_')
                i = i + 1
        else:
            output[name[:-1]] = element
    flatten(x)
    return output


#Transforms a JSON file into a dict, then flattens the dict
def load_flat_json(file: str) -> dict:
    with open(file, 'r') as j_data:
        j_dict = json.load(j_data)
        return flatten_json(j_dict)

#Flattens Directory of Jsons into a CSV
def jsons_to_csv(json_dir: str, output_path: str):
    json_files = [os.path.join(json_dir, file) for file in os.listdir(json_dir)]
    json_dicts = list(map(load_flat_json, json_files))
    temp_csv = os.path.dirname(output_path) + '\\temp.csv'

    #Creating Headers
    keys = []
    with open(temp_csv, 'w', newline = '') as fin:
        for jd in json_dicts:
            #Appends new header for non-consistent JSON fields
            for key in jd:
                if key not in keys:
                    keys.append(key)
            #Writing data
            csv_writer = csv.DictWriter(fin, fieldnames=keys)
            csv_writer.writerow(jd)

    with open(temp_csv, 'r') as fout:
        text = fout.read()

    #Prepending headers to CSV
    with open(output_path, 'a') as fin:
        fin.write(f"{','.join(keys)}\n")
        fin.write(text)

    os.remove(temp_csv)



