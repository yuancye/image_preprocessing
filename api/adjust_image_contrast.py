'''
@author: Carlos
purpose:
    Adjust images contrast and brightness.dd

input:
    Images are loacted under "images" folder
            
output:
    Adjusted images located under "images-adj"
'''

import os, cv2
from PIL import Image
import numpy as np
from skimage import exposure
from typing import List
from pathlib import Path

def auto_adjust(images_dir: Path, output_dir: Path, image_types: List[str] = ['.jpg', '.png']) ->None:
    for root, folder, files in os.walk(images_dir):
        for file in files:
            ext = os.path.splitext(file)[1]  
            if ext in image_types:
                file_path = os.path.join(root, file)
                img = Image.open(file_path)
                array = np.asarray(img)
                p2, p98 = np.percentile(array, (2, 98))
                array_new = exposure.rescale_intensity(array, in_range=(p2, p98))

                img_new = Image.fromarray(array_new)
                img_new.save(output_dir + '/' + file)

def manual_adjust(images_dir: Path, output_dir: Path, image_types: List[str] = ['.jpg', '.png'])->None:
    for root, folder, files in os.walk(images_dir):
        for file in files:
            ext = os.path.splitext(file)[1]  
            if ext in image_types:
                file_path = os.path.join(root, file)

                img = cv2.imread(file_path)

                cv2.namedWindow(file, cv2.WINDOW_NORMAL) 
                cv2.resizeWindow(file, 700, 700)
                cv2.imshow(file, img)
                k = cv2.waitKey(0)
            
                arr = np.asarray(img)
                value = 10

                cv2.namedWindow("new", cv2.WINDOW_NORMAL) 
                cv2.resizeWindow("new", 700, 700)
                adjust = True
                while adjust:
                    if k == ord('b'): #increase brightness
                        arr = np.where((255-arr) < value, 255, arr+value)

                    if k == ord('d'): #decrease brightness
                        arr = np.where((0 + arr) < value, 0, arr-value)

                    if k == ord('z'): #decrease contrast
                        p2, p98 = np.percentile(arr, (2, 98))
                        arr = exposure.rescale_intensity(arr, in_range=(p2, p98))

                    if k == ord('v'): #reload image
                        arr = np.asarray(img)

                    if k == ord('s'): #save image
                        img_new = Image.fromarray(arr)
                        img_new.save(output_dir + '/' + file)
                        cv2.destroyAllWindows()
                        break

                    if k == ord('q'): #quit
                        cv2.destroyAllWindows()
                        adjust = False
                        return

                    cv2.imshow("new", arr)  
                    k = cv2.waitKey(0)

def adjust_contrast(images_dir: Path, output_dir: Path, image_types: List[str] = ['.jpg', '.png'], auto: bool = False):
    if auto:
        auto_adjust(images_dir, output_dir, image_types)
        return
    manual_adjust(images_dir, output_dir, image_types)

