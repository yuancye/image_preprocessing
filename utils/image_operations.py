import os, shutil

def move_image(src, des, file):
    """
    The function `move_image` moves an image file from a source directory to a destination directory.
    
    :param src: The source directory where the image file is currently located
    :param des: The parameter "des" in the function "move_image" represents the destination directory
    where the image file will be moved to
    :param file: The `file` parameter is the name of the image file that you want to move from the
    source directory (`src`) to the destination directory (`des`)
    """
    image_path = os.path.join(src, file) 
    des_path = os.path.join(des, file)
    if not os.path.exists(des_path):   
        shutil.move(image_path, des)

def copy_image(src, des, file):
    src_path = os.path.join(src, file) 
    des_path = os.path.join(des, file)
    if not os.path.exists(des_path):   
        shutil.copy(src_path, des_path)
