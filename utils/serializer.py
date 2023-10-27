import json, csv, pickle
from typing import List, Dict
from pathlib import Path 
import pandas as pd

def save_to_json(output_path: Path, data: Dict) ->None:
    with open(output_path, 'w') as output:
        json.dump(data, output)

def save_2darray_to_txt(ouput_path: Path, array_2d: List[List[float]]):
    with open(ouput_path, 'w') as output:
        for row in array_2d:
            list1 =[(str(item) + " ") for item in row]
            output.writelines(list1)
            output.write('\n')
        # output.write('\n'.join([' '.join(i) for i in array_2d]))

def save_list_to_csv(filename_list: List[str], output_filename: str)->None:
    if len(filename_list) > 0:
        df = pd.DataFrame({"file_name" : filename_list})
        df.to_csv(output_filename, index = None, header=None)
            
def save_dic_to_csv(dict: Dict, csv_file_path: Path):
    """
    The function `save_dic_to_csv` takes a dictionary of grouped files and saves the key and counts of value
    to a CSV file.
    
    :param dict: dict is a dictionary where the keys are prefixes and the values are
    lists of suffixes
    :param csv_file_name: The name of the CSV file you want to save the data to
    """

    # Create flattened data with key and count of values
    flattened_data = [{'Prefix': key, 'Count': len(suffixes)} for key, suffixes in dict.items()]
    
    # Save the flattened_data to a CSV file  
    with open(csv_file_path, 'w', newline='') as file:
        fieldnames = ['Prefix', 'Count']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)


def save_image_id(image_id_logger_path: Path, data: int):
    with open(image_id_logger_path, 'w') as f:
        f.write(data)


def save_to_pickle(pickle_filepath, data, **kwargs):
    with open(pickle_filepath, 'wb') as output:
        pickle.dump(data, output, **kwargs)
