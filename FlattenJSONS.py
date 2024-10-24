import json
import os
import csv
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Takes a json and flattens all fields into a dictionary, which is then used to write to a csv."
    )

    parser.add_argument("Input_Path",
                        help="The path to a JSON file or directory containing JSON files.")
    parser.add_argument("Output_Path",
                        help="A CSV file to which data is written.")
    parser.add_argument("-t",
                        "--Trim_Headers",
                        default=False,
                        action="store_true",
                        help="Removes prefixes indicating the level of JSON indentation on headers.")
    
    args = parser.parse_args()
    
    jsons_to_csv(args.Input_Path, args.Output_Path, args.Trim_Headers)


def jsons_to_csv(input_path: str, output_path: str, remove_header_prefix: bool = False):
    # Reading path data
    if os.path.isdir(input_path):
        json_files = [os.path.join(input_path, file) for file in os.listdir(input_path)]
    else: 
        json_files = input_path
    json_dicts = list(map(load_flat_json, json_files))
    temp_csv = '.\\temp.csv'
    headers = json_fields_to_headers(json_dicts)

    # Writing data
    with open(temp_csv, 'w', newline='') as fin:
        for jd, in json_dicts:
            csv_writer = csv.DictWriter(fin, fieldnames=headers)
            csv_writer.writerow(jd)
    
    with open(temp_csv, 'r') as fout:
        text = fout.read()

    # Prepending headers to CSV
    fout = open(output_path, 'a') if os.path.exists(output_path) else open(output_path, 'x')
    if remove_header_prefix:
        headers = [key.split('_')[-1] for key in headers]
        headers = keys_from_list(headers)
    fout.write(f"{','.join(headers)}\n")
    fout.write(text)
    fout.close()

    os.remove(temp_csv)


# Transforms a JSON file into a dict, then flattens the dict
def load_flat_json(file: str) -> dict:
    with open(file, 'r') as j_data:
        j_dict = json.load(j_data)
        return flatten_json(j_dict)


# Iterates through the JSON fields and places them in a dict. Recurses if the field is a dict or list.
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


# Creates a header for a given json field. Appends a new header for jsons with inconsistent fields
def json_fields_to_headers(json_dicts: list[dict]) -> list:
    keys = []
    for jd in json_dicts:
        for key in jd:
            if key not in keys:
                keys.append(key)
    return keys


# Checks for duplicate elements in a list and appends a suffix on duplicates to make them unique.
def keys_from_list(x: list) -> list:
    y = x.copy()
    occurrences = {i: y.count(i) for i in y}
    for k, v in occurrences.items():
        count = v
        if v <= 1:
            continue
        for i in range(len(y)):
            if y[i] == k:
                if v - count == 0:
                    count -= 1
                else:
                    y[i] = str(y[i]) + "_" + str(v - count)
                    count -= 1    
    return y


if __name__ == "__main__":
    main()






