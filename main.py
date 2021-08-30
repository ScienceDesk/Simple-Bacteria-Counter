##  Required imports
import matplotlib; matplotlib.use('Agg')
from sdesk.proc import io
import cv2
import numpy
import imutils
from PIL import Image
##


def count_bacteria(image: numpy.ndarray) -> int:
    return len(cnts)


# Define your method main()
def main():
    # LOAD INPUT FILE
    loader = io.DataLoader()
    sdesk_input_file = loader.files[0]
    
    # PROCESS THE INPUT FILE AND PRODUCE RESULTS
    file_name = file_metadata['name']
    image = cv2.imread(sdesk_input_file.path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 3, 5, 5)
    edged = cv2.Canny(blurred, 50, 100)
    a,b = (3, 2)
    kernel_ab = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (a, b))
    kernel_ba = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (b, a))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel_ab)
    closed = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, kernel_ba)

    cnts = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    out_image = cv2.drawContours(image, cnts, -1, (0, 0, 255), 1)
    number_of_bacteria = len(cnts)

    # UPDATE CUSTOM METADATA OF INPUT FILE
    new_custom_properties = {**sdesk_input_file.custom_properties}
    new_custom_properties['number of bacteria'] = number_of_bacteria
    sdesk_input_file.update_custom_properties(new_custom_properties)
    
    # CREATE THE OUTPUT FILES - THEY WILL DERIVE FROM THE INPUT FILE
    im = Image.fromarray(out_image)
    output_file_name = file_name + "_segmentation.png"
    sdesk_output_file = io.create_output_file(output_file_name)
    im.save(sdesk_output_file.path())



# Call method main()
main()