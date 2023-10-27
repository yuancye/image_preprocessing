import os, shutil, subprocess
import pandas as pd
from PIL import Image
from typing import  List
from pathlib import Path

def extract_images(data_dir: Path, video_datasets_path: Path, output_folder: Path, csv_dir: Path, csv_name: str) ->None:  
    """
    The function `extract_images` takes in a directory path, a video dataset path, an output folder
    path, a CSV directory path, and a CSV name, and extracts images from the video datasets, saves them
    in the output folder, and updates a CSV file with the image names and their corresponding file
    paths.
    
    :param data_dir: The `data_dir` parameter is the directory where the the name of the extracted images 
    will be splitted from the path
    :type data_dir: Path
    :param video_datasets_path: The `video_datasets_path` parameter is the path to the directory that
    contains the video datasets
    :type video_datasets_path: Path
    :param output_folder: The `output_folder` parameter is the path to the folder where the extracted
    images will be saved
    :type output_folder: Path
    :param csv_dir: The `csv_dir` parameter is the directory where the CSV file is located or where it
    should be created if it doesn't exist
    :type csv_dir: Path
    :param csv_name: The `csv_name` parameter is a string that represents the name of the CSV file that
    will be created or updated
    :type csv_name: str
    """
    prefix = os.path.splitext(os.path.basename(video_datasets_path))[0]    
    image_ls = []
    file_path_ls = []
    #loop through video_datasets
    for folder in os.listdir(video_datasets_path):
        main_folder_path = os.path.join(video_datasets_path, folder)
        count_ls = [0] # can be passed in as a reference
        extract_images_helper(data_dir, main_folder_path, output_folder, prefix, count_ls, image_ls, file_path_ls)
    #read and update csv
    # base_dir = os.path.dirname(video_datasets_path)
    csv_path = os.path.join(csv_dir, csv_name)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else: 
        df = pd.DataFrame()
    dict = {'image_name' : image_ls, 'full_path' : file_path_ls}
    new_df = pd.DataFrame(dict)
    df = pd.concat([df, new_df], ignore_index = True)
    df.to_csv(csv_path, index=False)

def extract_images_helper(data_dir, main_folder_path, output_folder, prefix, count_ls, image_ls, file_path_ls):
    # Get the name of the main folder
    file_name = os.path.basename(main_folder_path)
    main_folder_name = os.path.splitext(file_name)[0]
   

    if is_compressed_file(file_name):
        # Extract the images from the compressed main folder
        extract_images_from_compressed(data_dir, main_folder_path, output_folder, main_folder_name, prefix, count_ls, image_ls, file_path_ls)
    else:
        # Extract the images from the uncompressed main folder
        count_ls[0] = count_ls[0] + 1
        extract_images_from_folder(data_dir, main_folder_path, output_folder, main_folder_name, prefix, count_ls, image_ls, file_path_ls)

def extract_images_from_compressed(data_dir, compressed_file_path, output_folder, main_folder_name, prefix, count_ls, image_ls, file_path_ls):   
    compressed_folder_name = os.path.splitext(os.path.basename(compressed_file_path))[0]
    temp_folder = os.path.join(os.path.dirname(compressed_file_path), compressed_folder_name)
    os.makedirs(temp_folder, exist_ok=True)

    unpack_file(compressed_file_path, temp_folder)

    extract_images_from_folder(data_dir, temp_folder, output_folder, main_folder_name, prefix, count_ls, image_ls, file_path_ls)

    shutil.rmtree(temp_folder)

def extract_images_from_folder(data_dir, folder_path, output_folder, main_folder_name, prefix, count_ls, image_ls, file_path_ls):
    for root, _, files in os.walk(folder_path):
        saved = False
        for file in files:
            file_path = os.path.join(root, file)
            if is_compressed_file(file):                 
                extract_images_from_compressed(data_dir, file_path, output_folder, main_folder_name, prefix, count_ls, image_ls, file_path_ls)            
        
            elif is_image_file(file_path) and file.lower().endswith('.gif'):              
                gif_image = Image.open(file_path)
                for frame_number in range(gif_image.n_frames):
                    extract_gif(output_folder, main_folder_name, prefix, count_ls, image_ls, file, gif_image, frame_number)
                    save_filepath(file_path_ls, file_path)
                saved = True

            elif is_image_file(file_path):
                extract_single_image(output_folder, main_folder_name, prefix, count_ls, image_ls, file, file_path)
                save_filepath(file_path_ls, file_path, data_dir)           
                saved = True
        if saved:
            count_ls[0] += 1

def save_filepath(file_path_ls, file_path, data_dir):
    saved_file_path = os.path.relpath(file_path, data_dir)
    file_path_ls.append(saved_file_path)

def extract_single_image(output_folder, main_folder_name, prefix, count_ls, image_ls, file, file_path):
    file_pre = os.path.splitext(file)[0]
    if '.' in file:
        file_pre = file_pre.split('.')[-1]
    ext = os.path.splitext(file)[1]
    if 'webp' in ext:
        ext = '.jpg'
    file_name = file_pre + ext
    new_file_name = f"{prefix}_{main_folder_name}_{str(count_ls[0])}_{file_name}"
    shutil.copy2(file_path, os.path.join(output_folder, new_file_name))
    image_ls.append(new_file_name)

def extract_gif(output_folder, main_folder_name, prefix, count_ls, image_ls, file, gif_image, frame_number):
    gif_image.seek(frame_number)
    frame = gif_image.copy()   
    file_prefix = os.path.splitext(file)[0] 
    frame_filename = f'{frame_number}.png'  
    new_file_name = f"{prefix}_{main_folder_name}_{str(count_ls[0])}_{file_prefix}_{frame_filename}"
    frame_path = os.path.join(output_folder, new_file_name)
    frame.save(frame_path)
    image_ls.append(new_file_name)

def is_compressed_file(file_name):
    archive_extensions = ['.zip', '.rar', '.7z', '.gz', '.tar', '.bz2', '.xz', '.lzma']
    return any(ext in file_name.lower() for ext in archive_extensions)

def unpack_file(compressed_file, destination_folder):
    command = [r'C:\Program Files\7-Zip\7z.exe', 'x', compressed_file, '-o{}'.format(destination_folder)]
    # Execute the command using subprocess
    subprocess.run(command)

def is_image_file(file_path):
    exts = ['.svg', '.h5', '.hdf5']
    if any(ext in file_path.lower() for ext in exts):
        return False
    try:
        with Image.open(file_path) as img:
            return True
    except IOError:
        return False
    

