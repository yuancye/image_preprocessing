import json, pickle
from pathlib import Path 

def load_json(json_path):
    if Path(json_path).is_file(): 
        with open(json_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    return data

def load_image_id(image_id_logger_path, start_id = 100000000000):
    if Path(image_id_logger_path).is_file():
        with open(image_id_logger_path, 'r') as f:
            image_id = f.readline()
    else:
        image_id = start_id
    return int(image_id)


def load_bbox_from_yolo_txt(txt_path):
    bboxs = []
    try:
        with open(txt_path, "r") as file:
            for line in file:
                bbox = line.split()
                bboxs.extend([bbox[1:]])
        return bboxs
    except FileNotFoundError:
        print(f"The file '{txt_path}' does not exist.")
    except IOError as e:
        print(f"An error occurred while reading the file: {str(e)}")

def load_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data 