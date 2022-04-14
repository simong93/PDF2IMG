from pdf2image import convert_from_path
import math
from typing import Tuple, Union
import cv2
import numpy as np
from deskew import determine_skew
import shutil
from PIL import Image
import os

class Convert:

    def __init__(self,PDF_file):
        if PDF_file == "Done":
            return
        else:
            self.Main(PDF_file)

    def Main(self,PDF_file):
        for Coverted in self.ConvertPDFPages(PDF_file):

            image = cv2.imread(Coverted)
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            angle = determine_skew(grayscale)
            rotated = self.rotate(image, angle, (0, 0, 0))

            cv2.imwrite(Coverted, rotated)

        LocationMove = "RawFiles/" + PDF_file
        shutil.move(LocationMove, "RawFiles/Done")

    def rotate(self,image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]) -> np.ndarray:
        old_width, old_height = image.shape[:2]
        angle_radian = math.radians(angle)
        width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
        height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rot_mat[1, 2] += (width - old_width) / 2
        rot_mat[0, 2] += (height - old_height) / 2
        return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

    def CropPages(self,filename):
        '''
        Resize the image so they are all the same size
        '''
        img = Image.open(filename)
        new_img = img.resize((1000, 1500))
        new_img.save(filename, "JPEG", optimize=True)

    def ConvertPDFPages(self,PDF_file):

        # Create a varible to store page names
        ConvertedPages = []

        # Store all the pages of the PDF in a variable
        location = "RawFiles/" + PDF_file
        pages = convert_from_path(location, 500)

        # Counter to store images of each page of PDF to image
        image_counter = 1

        # Directory
        locationmake = "Converted/" + PDF_file.replace(".pdf","")

        # Parent Directory path
        parent_dir = os.getcwd()

        # Path
        path = os.path.join(parent_dir, locationmake)
        print(path)

        print("Make directory",path)
        os.mkdir(path)
        print("Make directory done")

        # Iterate through all the pages stored above
        for page in pages:

            PDF_file = PDF_file.replace(".pdf","")
            filename = PDF_file + " page " + str(image_counter) + ".jpg"

            # Save the image of the page in system
            SaveLocation = "Converted/" + PDF_file + "/" + filename
            page.save(SaveLocation, 'JPEG')

            # Increment the counter to update filename
            image_counter = image_counter + 1

            #Resize the image so they are ready
            self.CropPages(SaveLocation)

            #Stores Pages names for later
            ConvertedPages.append(SaveLocation)

        return ConvertedPages