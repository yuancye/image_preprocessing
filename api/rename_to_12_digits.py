'''
update image id to the vertex training 12 digit ids
save a json file that map the old image name to the new image id.
save a json file that map the new image name to the old image id.
'''
import os
from typing import List, Dict
from pathlib import Path
from utils.serializer import save_to_json, save_image_id
from utils.deserializer import load_image_id


def rename_imgs_to_12d(img_folder_path: Path, rsc_json_path: Path, img_id_logger_path: Path, image_types: List[str]=['.jpg', '.png'], output_img_ext: str='.jpg') ->Dict:
    """
    The function `rename_imgs_to_12d` renames images in a specified folder and its subfolders to a 12-digit format and
    saves the mapping of old and new image names in JSON files.
    
    :param img_folder_path: The path to the folder containing the images that you want to rename
    :type img_folder_path: Path
    :param rsc_json_path: The `rsc_json_path` parameter is the path to the JSON file where the image
    name mappings will be saved
    :type rsc_json_path: Path
    :param img_id_logger_path: The `img_id_logger_path` parameter is the path to a file that logs the
    next available image ID. This file is used to keep track of the image IDs and ensure that each image is
    assigned a unique ID when it is renamed
    :type img_id_logger_path: Path
    :param image_types: The `image_types` parameter is a list of file extensions for the image files
    that you want to rename. By default, it is set to `['.jpg', '.png']`, which means it will only
    rename files with the extensions `.jpg` and `.png`
    :type image_types: List[str]
    :param output_img_ext: The `output_img_ext` parameter is a string that specifies the file extension
    for the renamed images. By default, it is set to '.jpg', but you can change it to any other valid
    image file extension like '.png', '.jpeg', etc, defaults to .jpg
    :type output_img_ext: str (optional)
    :return: The function `rename_imgs_to_12d` returns two dictionaries: `image_name_old_to_new` and
    `image_name_new_to_old`.
    """
    image_name_old_to_new = {}
    image_name_new_to_old = {}
    img_id = load_image_id(img_id_logger_path)
    count = 0

    for root, folder, files in os.walk(img_folder_path):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in image_types:
                split_ext = os.path.splitext(file)
                img_basename = split_ext[0]

                #rename img                 
                img_path = os.path.join(root, file)
                new_img_name = str(img_id) + output_img_ext           
                new_img_path = os.path.join(root, new_img_name)
                os.rename(img_path, new_img_path)

                image_name_old_to_new[img_basename] = img_id
                image_name_new_to_old[img_id] = img_basename
                img_id += 1
                count += 1  

    print(f"{count} images have been renamed!")
    des_json_path_old = compose_output_json_path(rsc_json_path, str(count) + '-old-to-new')
    des_json_path_new = compose_output_json_path(rsc_json_path, str(count) + '-new-to-old')
    save_to_json(des_json_path_old, image_name_old_to_new)
    save_to_json(des_json_path_new, image_name_new_to_old)
    save_image_id(img_id_logger_path, str(img_id)) 

    return image_name_old_to_new, image_name_new_to_old


def compose_output_json_path(rsc_json_path: Path, count):
    basename = os.path.basename(rsc_json_path)
    directory = os.path.dirname(rsc_json_path)
    basename_list = os.path.splitext(basename)
    outputname = basename_list[0] +'-' + str(count) + basename_list[1] 
    des_json_path = os.path.join(directory, outputname)
    return des_json_path

