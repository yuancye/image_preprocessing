import os

def create_dir(base_dir, dir_name):
    path = os.path.join(base_dir, dir_name)
    os.makedirs(path, exist_ok=True)
    return path

