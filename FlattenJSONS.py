import json
import os
import csv
import argparse

def flatten_json(x: dict) -> dict:
    output = {}

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
                i += 1
        else:
            output[name[:-1]] = element
    flatten(x)
    return output


#Transforms a JSON file into a dict, then flattens the dict
def load_flat_json(file: str) -> dict:
    with open(file, 'r') as j_data:
        j_dict = json.load(j_data)
        return flatten_json(j_dict)


#Creates a header for given json_data. Appends a new header for jsons with inconsistent headers.
def json_fields_to_headers(json_dicts: list[dict]) -> list:
    keys = []
    for jd in json_dicts:
        for key in jd:
            if key not in keys:
                keys.append(key)
    return keys


#Flattens Directory of Jsons into a CSV
def jsons_to_csv(input_path: str, output_path: str, remove_header_prefix: bool = False):

    # Reading path data
    if os.path.isdir(input_path):
        json_files = [os.path.join(input_path, file) for file in os.listdir(input_path)]
    else:
        json_files = [input_path]
    json_dicts = list(map(load_flat_json, json_files))
    temp_csv = os.path.dirname(output_path) + '\\temp.csv'
    headers = json_fields_to_headers(json_dicts)

    #Writing Data
    with open(temp_csv, 'w', newline = '') as fin:
        for jd in json_dicts:
            csv_writer = csv.DictWriter(fin, fieldnames=headers)
            csv_writer.writerow(jd)

    with open(temp_csv, 'r') as fout:
        text = fout.read()

    #Prepending headers to CSV
    with open(output_path, 'a') as fin:
        if remove_header_prefix:
            headers = [key.split('_')[-1] for key in headers]
        fin.write(f"{','.join(headers)}\n")
        fin.write(text)

    os.remove(temp_csv)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("Input_Path", help="A JSON file or directory containing jsons.")
    parser.add_argument("Output_Path", help="A CSV file to which data is written.")
    parser.add_argument("-t", "--Trim_Headers", default=False, action="store_true", help="Removes prefixes indicating level of JSON indentation on headers.")
    args = parser.parse_args()

    jsons_to_csv(args.Input_Path, args.Output_Path, args.Trim_Headers)


if __name__ == "__main__":
    main()



