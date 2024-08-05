# Copyright Lars Quentin, Klara Henrike Frahnert 2024
# License: MIT

import os
import shutil
import sys
import time

from ij import IJ, ImagePlus

# What does this tool do? - It segments multiple picturs with a pre-trained classifyer and than counts the selected structurs.
#	If you also apply the 'get_counts.py' tool these results will be transfered into a excel sheet.
# required folder structure: not more than one level of subfolders. In each folder you putt together the pictures (tif, 
# 	otherwise you need to adjust the script accordingly) you want together with all the classifyers you want to put one them 
# 	(each classifyer will be applyed on each picture individually).
#	It might be necessary that the folder is localy saved on your computer (e.g. on the desctop).
# create a classifyer: open a representative picture in Labkit (preinstalled plugin in Fiji). Train a classifyer by giving 
#	examples of for- and background. Save the classifyer into the folder with the picturs.
# necessary adjustments in the script: folder path (line24), pixel threshold (lines 29 - 30)
# result export into excel: Make sure Python is installed on your computer. Save a copy of 'get_counts.py' in your folder where the subfolders are and run. 
# duration: depends heavily on your computer, number of picturs and classifyers, should be around 10 - 20 seconds per picture.
#	duration will be given out at the end of the script.

PATH_OF_ALL_EXPERIMENTS = r"\\ug-uyst-ba-cifs.student.uni-goettingen.de\home\users\klara.frahnert\Desktop\PRO067_senescence\PRO067_72h"
# defines the folder where the different subfolders are.
IMAGE_FILEEXTENSION = "tif"
# defines the picture format

THRESHOLD_PIXEL_SQUARED_MIN = "150"
THRESHOLD_PIXEL_SQUARED_MAX = "1000000"
# sets a threshold for counting the selected pixels

start = time.time()

def find_all_subfolders_with_at_least_one_classifier():
  # find all folders
  folders = []
  for filename in os.listdir(PATH_OF_ALL_EXPERIMENTS):
    full_path = os.path.join(PATH_OF_ALL_EXPERIMENTS, filename)
    if os.path.isdir(full_path):
      folders.append(full_path)
  
  # check which ones have at least one classifier in them
  folders_with_classifiers = []
  for folder in folders:
    has_any_classifier = False
    for filename in os.listdir(folder):
      file_extension = filename.split(".")[-1]
      if file_extension.lower() == "classifier":
        has_any_classifier = True
    if has_any_classifier:
      folders_with_classifiers.append(folder)
  return folders_with_classifiers


def find_classifiers(folder):
  return_values = []
  for filename in os.listdir(folder):
    extension = filename.split(".")[-1].lower()
    if extension == "classifier":
      return_values.append(os.path.join(folder, filename))
  return return_values

def run_segmentation(folder, classifier):
  print("Running " + folder + " with classifier " + classifier)
  
  # First, create the folder with the results
  # if it exist, delete it first
  classifier_name_with_extension = os.path.basename(classifier)
  classifier_name = classifier_name_with_extension.split(".")[0]
  output_foldername = os.path.join(folder, classifier_name)
  
  if os.path.exists(output_foldername):
    print(output_foldername + " already exists. Deleting...")
    shutil.rmtree(output_foldername)
  os.mkdir(output_foldername)
  
  # Find all images in folder
  all_image_paths = []
  for filename in os.listdir(folder):
    file_extension = filename.split(".")[-1]
    if file_extension == IMAGE_FILEEXTENSION:
      all_image_paths.append(os.path.join(folder, filename))
  
  for image_path in all_image_paths:
    # load img
    imp = IJ.openImage(image_path)
    
    # run labkit
    # expects the image to literally be open
    imp.show()
    IJ.run(imp, "Segment Image With Labkit", "segmenter_file=" + classifier + " use_gpu=false")
    segmentation_img = IJ.getImage()
    imp.close()
    
    # Run threshold and save img
    IJ.run(segmentation_img, "Auto Threshold", "method=Default white")
    threshold_img = IJ.getImage()
    
    image_name_with_extension = os.path.basename(image_path)
    image_name_without_extension = image_name_with_extension.split(".")[0]
    threshold_path_with_extension = output_foldername + os.path.sep + "threshold_" + image_name_with_extension
    threshold_path_without_extension = output_foldername + os.path.sep + "threshold_" + image_name_without_extension
    
    IJ.save(threshold_img, threshold_path_with_extension)
    threshold_img.close()
    
    # reload img
    threshold_img = IJ.openImage(threshold_path_with_extension)
    IJ.run(threshold_img, "Analyze Particles...", "size=" + THRESHOLD_PIXEL_SQUARED_MIN + "-" + THRESHOLD_PIXEL_SQUARED_MAX + " show=Nothing clear pixel summarize")
    IJ.saveAs("Results", threshold_path_without_extension + ".txt")
    IJ.run("Close")
    #print(threshold_path_without_extension + ".txt")
    #sys.exit(0)

all_folders = find_all_subfolders_with_at_least_one_classifier()

for folder in all_folders:
  for classifier in find_classifiers(folder):
    run_segmentation(folder, classifier)


end = time.time()
print("Took " + str(end-start) + " seconds!")
# gives out how long the script took to run
