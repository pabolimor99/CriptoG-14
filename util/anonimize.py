from datetime import datetime
import pydicom

def save_dicom(image, original_dicom, output_path):
    """
    Guarda una imagen como archivo DICOM con los metadatos originales,
    pero permite anonimizar los datos del paciente.
    """

    new_dicom = original_dicom.copy()
    new_dicom.PixelData = image.tobytes()
    new_dicom.Rows, new_dicom.Columns = image.shape
    new_dicom.BitsAllocated = 16
    new_dicom.SamplesPerPixel = 1
    new_dicom.PhotometricInterpretation = 'MONOCHROME2'
    new_dicom.PixelRepresentation = 0
 
    sensitive_tags = [
        (0x0010, 0x0010),  # Patient's Name
        (0x0010, 0x0020),  # Patient ID
        (0x0010, 0x0030),  # Patient's Birth Date
        (0x0010, 0x0040),  # Patient's Sex
        (0x0008, 0x0020),  # Study Date
        (0x0008, 0x0021),  # Series Date
        (0x0008, 0x0022),  # Acquisition Date
        (0x0008, 0x0023),  # Content Date
        (0x0008, 0x0030),  # Study Time
        (0x0008, 0x0080),  # Institution Name
        (0x0008,0x0013),   # Instance Creation Date
        (0x0008,0x0032),       # Acquisition Time
        (0x0008,0x0070), #Manufacturer: "Agfa Healthcare"
        (0x0008,0x1090), #Manufacturer's Model Name: "DX-G"
        (0x0018,0x1000), #Device Serial Number: "123456"


    ]
    
    for tag in sensitive_tags:
            if tag in new_dicom:
                del new_dicom[tag]


    new_dicom.Modality = 'OT'
    new_dicom.SeriesDescription = 'Imagen Anonimizada'
    new_dicom.InstanceCreationDate = datetime.now().strftime('%Y%m%d')
    new_dicom.InstanceCreationTime = datetime.now().strftime('%H%M%S')

    new_dicom.save_as(output_path)
    print(f"Imagen guardada como DICOM en: {output_path}")

if __name__ == "__main__":

    dicom_path = './images/I1000000.dcm'

    dicom = pydicom.dcmread(dicom_path)

    image = dicom.pixel_array

    save_dicom(image, dicom, './images/I1000000_2.dcm')