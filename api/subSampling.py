import re, random, os
from utils.image_operations import copy_image
from utils.register import create_dir
from typing import List, Pattern, Dict
from pathlib import Path

def subSampling(image_dir: Path, subsample_dir: Path, pattern: Pattern, num_files: List[int], image_types: List[str] = ['.jpg', '.png']) ->None:
    """
    The function `sub_sampling` takes an image directory, a subsample directory, a pattern, a list of
    numbers of files to select, and an optional list of image types, and performs subsampling by
    randomly selecting a specified number of files from each group defined by the pattern and copying
    them to the subsample directory.
    
    :param image_dir: The directory where the original images are located
    :type image_dir: Path
    :param subsample_dir: The `subsample_dir` parameter is the directory where the subsampled images
    will be saved
    :type subsample_dir: Path
    :param pattern: The "pattern" parameter is a regular expression pattern used to group filenames. It
    is used to group the files based on a specific pattern. For example, if the pattern is set to
    r'^(.*?)(_frame_)(.*?)$',it will group files based on str *_frame_.
    :type pattern: Pattern
    :param num_files: The `num_files` parameter is a list of integers that specifies the number of files
    to be randomly selected from each group of files. Each group is determined by the `pattern`
    parameter, which is a regular expression pattern used to group filenames together.
    :type num_files: List[int]
    :param image_types: The `image_types` parameter is a list of strings that specifies the file
    extensions of the image files to be considered for sub-sampling. By default, it is set to ['.jpg',
    '.png'], which means that only files with the extensions '.jpg' and '.png' will be considered
    :type image_types: List[str]
    :return: The function is not returning anything.
    """
    for root, folders, files in os.walk(image_dir):
        image_files = []
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in image_types:
                image_files.append(file)
        if len(image_files) > 0:
            grouped_files_dic = group_filenames(image_files, pattern)
            for num in num_files:
                selected_files = random_select_files(grouped_files_dic, num_files= num)
                des_dir = create_dir(subsample_dir, str(num))
                copy_files(root, des_dir, selected_files)

    return

def group_filenames(filenames: List[str], pattern: Pattern) -> Dict:
    """
    The function `group_filenames` takes a list of filenames and groups them based on a common prefix
    and number pattern in the filename.
    
    :param filenames: The parameter "filenames" is a list of strings representing file names
    :return: The function `group_filenames` returns a dictionary where the keys are the prefixes and
    numbers extracted from the filenames, and the values are lists of filenames that have the same
    prefix and number.
    """
    grouped_files = {}

    for filename in filenames:
        # Use re.match to find matches in the filename
        match = re.match(pattern, filename)

        if match:
            prefix = match.group(1)
            number = match.group(2)
            # suffix = match.group(3)
            key = f"{prefix}{number}"
            grouped_files.setdefault(key, []).append(filename)

    return grouped_files

def random_select_files(grouped_files: Dict, num_files: int) ->List:
    selected_files = []
    for filenames in grouped_files.values():
        # Randomly sample 'num_files' from the filenames list
        selected_files.extend(random.sample(filenames, min(len(filenames), num_files)))
    return selected_files

def copy_files(src_dir: Path, des_dir: Path, filenames_list: List[Path]) ->None:
    for item in filenames_list:
        copy_image(src_dir, des_dir, item) 


