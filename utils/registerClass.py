import os
import shutil
from pathlib import Path
 
#Folder name can not be the same even if the new folder located in another base directory
class RegisterDir:

    def __init__(self) ->None:
        self.directories = {}

    def create(self, base_dir: Path, folder_name: str) ->Path:
        dir = os.path.join(base_dir, folder_name)
        if folder_name not in self.directories:
            dir = os.path.join(base_dir, folder_name)
            os.makedirs(dir, exist_ok=True)
            self.directories.update({folder_name : dir})
        return dir
    
    def delete(self, folder_name: str) ->bool:
        if folder_name in self.directories:
            dir = self.directories.get(folder_name)
            shutil.rmtree(dir)
            self.directories.pop(folder_name)
            return True
        
        print(f"{folder_name} does not exist")
        return False
        
    def update(self, cur_folder_name: str, new_folder_name: str) ->Path:
        try:
            cur_dir = self.directories.get(cur_folder_name)
            new_dir = self.add(os.path.dirname(cur_dir), new_folder_name)
            shutil.copytree(cur_dir, new_dir, dirs_exist_ok=True)
            print(f"Folder '{cur_folder_name}' has been renamed to '{new_folder_name}'.")
            self.directories.pop(cur_folder_name)
            shutil.rmtree(cur_dir)
            return new_dir
        except FileNotFoundError:
            print(f"The folder '{cur_folder_name}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def get(self, folder_name: str) ->Path:
        return self.directories.get(folder_name)


class FileListRegister:
    def __init__(self):
        self.registered_files = []

    def register_file(self, base_dir, file_name):
        file_path = os.path.join(base_dir, file_name)
        self.registered_files.append(file_path)

    def get_registered_files(self):
        return self.registered_files

def combine_files(file_paths, load_func, save_func, combined_file_path,  **save_func_kwargs):
    combined_data = {}

    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            data = load_func(file)
            combined_data.update(data)

    with open(combined_file_path, 'wb') as combined_file:
        save_func(combined_data, combined_file, **save_func_kwargs)

    print(len(combined_data))
    print(f"Combined data saved to {combined_file_path}")
