import os, json
import config

from utils.register import create_dir

from api import image_preprocessing


def extract_from_compressed():
    '''
    extract images from the given compressed files
    '''  
    csv_name = 'image_path_mapping.csv'
    video_datasets = os.path.join(config.DATA_DIR, 'video-datasets')
    output_image_folder = create_dir(config.DATA_DIR, '_images')
    image_preprocessing.extract_images_from_compressed_files(config.DATA_DIR, video_datasets, output_image_folder, config.RESULTS_DIR, csv_name)

def remove_match_image():
    '''
    remove images that its name contains the match
    '''
    image_folder_name = "_images"
    match_str = 'label'
    image_dir = os.path.join(config.DATA_DIR, image_folder_name)
    image_preprocessing.remove_matched_images(image_dir, match=match_str)

def extract_from_video():
    '''extract every xth image from the given video
    '''
    video_dir = os.path.join(config.DATA_DIR, "campos")
    image_dir = create_dir(config.DATA_DIR, "_images")
    image_preprocessing.extract_frames_from_video(video_dir, image_dir, video_type = ['.mp4', '.avi'], image_format = '.jpg', Xth = 100)

def subSample():
    '''sub_sampling images from source images
    '''
    src_folder = "231019-nature-frame-need-annotation-all"
    sample_folder = "images_subsample"
    num_files = [4]
    image_types = ['.jpg', '.png']
    # Define a regular expression pattern to match the filename
    pattern = r'^(.*?)(_\d{1,2}_)(.*?)$' #nature frame
    # pattern = r'^(.*?)(_\d+_)(.*?)$' # video_datasets
    # pattern = r'^(.*?)(_frame_)(.*?)$' # campos lab
    image_dir = create_dir(config.images, src_folder)
    subsample_dir = os.path.join(config.DATA_DIR, sample_folder)
    image_preprocessing.sub_sampling(image_dir, subsample_dir, pattern, num_files, image_types)

def remove_annotated():
    '''remove the images that has already been annotated
    '''
    image_folder = '231019-nature-frame-335'
    image_dir = os.path.join(config.images, image_folder)
    metadata_dir = os.path.join(config.META_DIR, 'nature-frames')
    load_func = json.load
    image_preprocessing.remove_annotated_images(image_dir, metadata_dir, load_func)

def renameto12d():
    ''' rename the images to 12 digits for livs training
    '''
    img_folder_name = "231019-nature-frame-335"
    img_folder_path = os.path.join(config.images, img_folder_name)  
    rsc_json_path = os.path.join(config.META_DIR, img_folder_name + '.json')
    img_id_logger = "image_id_logger.txt"
    img_id_logger_path = os.path.join(config.LOGS_DIR, img_id_logger)
    image_preprocessing.rename_images_to_12d(img_folder_path, rsc_json_path, img_id_logger_path, image_types=['.jpg', '.png'],  output_img_ext='.jpg',)

def adjust_contrast():
    '''adjust images contrast for annotation
    '''
    image_types= [".jpg"]
    image_source_dir = 'fine-adjust'
    image_src_dir = create_dir(config.DATA_DIR, image_source_dir)
    image_adj = create_dir(config.DATA_DIR, 'images_adj')
    # image_output_dir = create_dir(image_adj, image_source_dir)
    auto=False
    image_preprocessing.adjust_image_contrast(image_src_dir, image_adj, image_types, auto=auto)

def main():
    # extract_from_compressed()
    # remove_match_image()
    # extract_from_video()
    # subSample() 
    # remove_annotated()
    # renameto12d()
    adjust_contrast()

if __name__ == '__main__':
    main()