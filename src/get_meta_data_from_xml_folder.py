#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# =============================================================================
# Script that allows to extract the meta data from a folder containing xml files
# It takes as input a folder with a batch of xml files (CAPP, JuriCa, Ariane)
# extract all the meta data and returns a json file
# =============================================================================

# Basic imports
import os
import xml.etree.ElementTree as ET
import logging
import sys

# Import tqdm to have a loading bar
from tqdm import tqdm

# Set the logger
logging.basicConfig(filename="meta_data_extraction.log", level=logging.INFO)


# =============================================================================
# Reading and writing functions
# =============================================================================

def get_xml_files_from_directory(dir_path: str):
    """ Get all the xml files of a folder """
    list_of_files = os.listdir(dir_path)
    list_of_xml_files = [file for file in list_of_files if file.split(".")[1] == 'xml']
    return list_of_xml_files


# =============================================================================
# Functions to get the meta data
# =============================================================================

def get_meta_data_from_xml(xml_file: str, DATABASE_NAME: str):
    """
    Takes a the name of a single xml file set as input
    and parse it using a Breadth-first search
    to get all the meta data from the file
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    meta_data = BFS(root, DATABASE_NAME)
    return meta_data


def BFS(root, DATABASE_NAME):
    """
    Performs a Breadth-first search from the root of an xml file parsed with ET
    and returns a dictionary with the name of the tag of the and the value within the tag
    """
    out = dict()
    children = [child for child in root]

    # Special Case Ariane
    if DATABASE_NAME == "Ariane" and str(root.tag) == "Texte_Integral":
        return out

    # Special case Jurica
    if DATABASE_NAME == "JuriCa" and str(root.tag) == "TEXTE_ARRET":
        return out

    # Case CAPP
    if DATABASE_NAME == "CAPP" and str(root.tag) == "TEXTE":
        return out

    if not children:
        out[str(root.tag)] = str(root.text).strip() if root.text is not None else ""
        return out
    else:
        for child in root:
            out.update(BFS(root.find(child.tag), DATABASE_NAME))
        return out


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    # Get the folder path from the console
    input_folder_path = sys.argv[1]
    output_folder_path = sys.argv[2]
    DATABASE_NAME = sys.argv[3]

    # Stops the job if the input folder does not exist
    if not os.path.isdir(input_folder_path):
        sys.exit("The input path {} does not exist".format(input_folder_path))

    # Stops the job if the input folder does not exist
    if not os.path.isdir(output_folder_path):
        sys.exit("The output path {} does not exist".format(output_folder_path))

    # Stops the job if the DataBase name is not supported
    if DATABASE_NAME not in ["CAPP", "JuriCa", "Ariane"]:
        sys.exit("The database {} is not supported yet".format(DATABASE_NAME))

    ## Get the names of the xml files contained in the input folder
    list_of_xml_files = get_xml_files_from_directory(input_folder_path)

    # Print the beginning of the loop
    to_print = "#### Meta data extraction of the folder {} ####\n".format(input_folder_path)
    print(to_print)

    # Create an empty list to store the meta data of each file
    list_of_meta_data = []

    # Loop over each xml file, extract the meta data and put it into the meta data list
    for xml_file in tqdm(list_of_xml_files):
        try:
            # Get the meta data from the xml file
            meta_data = get_meta_data_from_xml(input_folder_path + xml_file, DATABASE_NAME)
            # Add the meta data to the list
            list_of_meta_data.append(meta_data)
            logging.info("file {} successfully read".format(xml_file))

        except Exception:
            logging.exception("problem reading the file {}".format(xml_file))

    # Save the results in a Json file
    import json

    output_file = "{}/{}_meta_data.json".format(output_folder_path, DATABASE_NAME)
    json.dump(list_of_meta_data, open(output_file, 'w'))
    print("\n#### File {} created".format(output_file))