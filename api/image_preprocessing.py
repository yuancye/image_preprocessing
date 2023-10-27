import os, shutil, cv2
from typing import Optional, Dict, Callable, List, Pattern
from pathlib import Path

from mesh_seg.extract_images_from_compressed_files import extract_images
from mesh_seg.subSampling import subSampling
from mesh_seg.rename_to_12_digits import rename_imgs_to_12d
from mesh_seg.adjust_image_contrast import adjust_contrast

def extract_frames_from_video(video_dir: Path, image_dir: Path, video_type: List[str]=['.mp4'], image_format: str='.jpg', Xth: int=100) ->None:
    """
    The function `extract_frames_from_video` takes a directory containing videos or dir that contains vidoes,
    extracts frames from each video at a specified interval, and saves the frames as images in a specified directory.
    
    :param video_dir: The directory where the videos are located
    :param image_dir: The directory where the extracted frames will be saved as images
    :param video_type: The video file extension, such as '.mp4' or '.avi', defaults to .mp4 (optional)
    :param image_format: The image format parameter specifies the format in which the extracted frames
    will be saved. In the given code, the default image format is set to '.jpg', defaults to .jpg
    (optional)
    :param Xth: The parameter "Xth" determines how often frames are extracted from the video. For
    example, if Xth is set to 100, then every 100th frame will be saved as an image, defaults to 100
    (optional)
    :return: nothing (None).
    """
    for root, folders, files in os.walk(video_dir):  
        for video in files:  
            split_ext = os.path.splitext(video)    
            if split_ext[1] in video_type:
                print("processing video ", video)
                video_path = os.path.join(root, video)
                video_name = os.path.basename(root) + '_' + os.path.splitext(video)[0]
                frame_count = 0
                cap = cv2.VideoCapture(video_path)                  
                #read until video is completed      
                while (cap.isOpened()):        
                    # Capture frame-by-frame
                    ret,frame = cap.read()
                    
                    if ret :                    
                        #save image every xth
                        if ((frame_count % Xth) == 0) :                          
                            image_name= video_name + '_frame_' + str(frame_count) + image_format
                            image_path = os.path.join(image_dir, image_name)
                            # writing the extracted images to the image_dir
                            cv2.imwrite(image_path, frame)                    
                        # increasing counter by 1
                        frame_count += 1
                    else:
                        break
                # Release all space and windows once done
                cap.release()
                cv2.destroyAllWindows() 
    return 


def extract_images_from_compressed_files(data_dir: Path, video_datasets_path: Path, output_folder: Path, csv_dir: Path, csv_name: str) ->None:  
    extract_images(data_dir, video_datasets_path, output_folder, csv_dir, csv_name)


def remove_matched_images(image_dir: Path, match = 'label') ->None:   
    image_removed_count = 0
    for root, folder, files in os.walk(image_dir):
        for file in files:
            if match in file:        
                image_to_remove_full_path = os.path.join(root, file)
                os.remove(image_to_remove_full_path)

                image_removed_count += 1

    print(f"{image_removed_count} images have been removed.")


def sub_sampling(image_dir: Path, subsample_dir: Path, pattern: Pattern, num_files: List[int], image_types: List[str] = ['.jpg', '.png']) ->None:
    subSampling(image_dir, subsample_dir, pattern, num_files, image_types)


def remove_annotated_images(image_dir: Path, metadata_dir: Path, load_func: Callable, load_func_kwargs: Optional[Dict] = {}) -> None:
    """
    The function `remove_annotated_images` removes images from a directory based on their presence in a
    metadata dictionary.
    
    :param image_dir: The directory where the images are stored
    :param metadata_dir: The directory where the metadata files are stored. These metadata files contain
    information about the images, {old_image_basename: new_ID}
    :param load_func: The load_func parameter is a function that is used to load the metadata from each
    file. It takes in a file object as its first argument and any additional keyword arguments specified
    in load_func_kwargs
    :param load_func_kwargs: `load_func_kwargs` is a dictionary that contains any additional keyword
    arguments that need to be passed to the `load_func` function. These keyword arguments are used to
    customize the behavior of the `load_func` function when loading the metadata from each file
    """
    metadata_dic = load_all_metadata(metadata_dir, load_func, load_func_kwargs)
    print(len(metadata_dic))
    image_removed_count = 0
    for root, _, images in os.walk(image_dir):
        for image in images:
            file_basename = os.path.splitext(image)[0]
            if file_basename in metadata_dic.keys():
                image_path = os.path.join(root, image)
                os.remove(image_path)
                image_removed_count += 1
    print(f"{image_removed_count} images have been removed.")


def load_all_metadata(metadata_dir, load_func, load_func_kwargs={}):
    """
    The function `load_all_metadata` loads metadata from multiple files in a directory using a specified
    loading function and returns the combined data.
    
    :param metadata_dir: The directory where the metadata files are located
    :param load_func: The load_func parameter is a function that is used to load the metadata from each
    file. It takes in a file object as its first argument and any additional keyword arguments specified
    in load_func_kwargs
    :param load_func_kwargs: `load_func_kwargs` is a dictionary that contains any additional keyword
    arguments that need to be passed to the `load_func` function. These keyword arguments are used to
    customize the behavior of the `load_func` function when loading the metadata from each file
    :return: a dictionary object named `combined_data` which contains the combined metadata from all the
    files in the `metadata_dir` or subdirectories.
    """
    combined_data = {}

    for root, folder, files in os.walk(metadata_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as file:
                data = load_func(file, **load_func_kwargs)
                combined_data.update(data)
    
    return combined_data


def rename_images_to_12d(img_folder_path: Path, rsc_json_path: Path, img_id_logger_path: Path, image_types: List[str]=['.jpg', '.png'], output_img_ext: str='.jpg') ->Dict:
    return rename_imgs_to_12d(img_folder_path, rsc_json_path, img_id_logger_path, image_types, output_img_ext)


def adjust_image_contrast(images_dir: Path, output_dir: Path, image_types: List[str] = ['.jpg', '.png'], auto: bool = False):
    adjust_contrast(images_dir, output_dir, image_types, auto)
