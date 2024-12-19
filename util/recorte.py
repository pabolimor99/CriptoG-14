import pydicom
import numpy as np

def load_dicom_image(file_path):

    dicom = pydicom.dcmread(file_path)
    return dicom, dicom.pixel_array

def crop_center(image, crop_size):

    h, w = image.shape
    crop_h, crop_w = crop_size
    
    start_h = (h - crop_h) // 2
    start_w = (w - crop_w) // 2
    
    return image[start_h:start_h + crop_h, start_w:start_w + crop_w]

import copy

def save_cropped_as_dicom(original_dicom, cropped_image, output_path):

    new_dicom = copy.deepcopy(original_dicom)

    new_dicom.PixelData = cropped_image.tobytes()

    new_dicom.Rows, new_dicom.Columns = cropped_image.shape

    new_dicom.save_as(output_path)

if __name__ == "__main__":

    dicom_file = "images\I1000000.dcm"
    
    crop_size = (512, 512)
    
    output_file = "images/imagen_recortada.dcm"
    
    original_dicom, image = load_dicom_image(dicom_file)

    cropped_image = crop_center(image, crop_size)
    
    save_cropped_as_dicom(original_dicom, cropped_image, output_file)
    
    print(f"Recorte guardado como DICOM en: {output_file}")
