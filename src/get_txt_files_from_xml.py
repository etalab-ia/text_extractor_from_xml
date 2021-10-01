#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# =============================================================================
# This script aims at extracting the legal text from
# a xml file containing.
# It takes as input a folder containing xml files
# and creates a folder a write *.txt files
# =============================================================================

# Libraries to import
import xml.etree.ElementTree as ET
import re
import os
import sys
import logging

# Additional library
from tqdm import tqdm

# Set the logger
logging.basicConfig(filename="text_extraction.log", level=logging.INFO)


# =============================================================================
# Simple reading and writing functions
# =============================================================================

def get_xml_files_from_directory(dir_path: str):
    """ Get all the xml files of a folder """
    list_of_files = os.listdir(dir_path)
    list_of_xml_files = [file for file in list_of_files if file.split(".")[1] == 'xml']
    return list_of_xml_files


def write_txt_to_file(inputText, outputPath):
    """ Write a string to a file"""
    text_file = open(outputPath, "w")
    text_file.write(inputText)
    text_file.close()


# =============================================================================
# Utils : writing and xml processing
# =============================================================================

def get_raw_text_from_xml_file(xml_file: str, DATABASE_NAME: str):
    """ Parse an xml and returns the text"""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # CAPP
    if DATABASE_NAME == "CAPP":
        contenu = root.find("TEXTE").find("BLOC_TEXTUEL").find("CONTENU")

    # JuriCa
    elif DATABASE_NAME == "JuriCa":
        contenu = root.find("TEXTE_ARRET")

    # Ariane
    elif DATABASE_NAME == "Ariane":
        contenu = root.find("Decision").find("Texte_Integral")

    # Read the raw string
    raw_string = ET.tostring(contenu, encoding='utf-8', method="xml")

    return raw_string.decode("utf-8")


# =============================================================================
# Text processing ro remove poorly encoded characters
# =============================================================================

def text_processing(string: str, DATABASE_NAME: str):
    """ main function that runs the cleaning steps """
    # Clean the xml tags
    text = replace_xml_tags(string, DATABASE_NAME)
    # Remove space encoded in utf
    text = replace_html_entities(text)
    # Remove the weird euro symbol
    text = replace_unicode_characters(text)
    return text


def replace_xml_tags(raw_text: str, DATABASE_NAME: str):
    """ Replace all the tags <example>  or </example> by \n """
    # Define and get the format of all the tags of the document
    pattern = r'(?<=\<).+?(?=\>)'
    tag_list = list(set(re.findall(pattern, raw_text)))
    tag_list = ["<" + tag + ">" for tag in tag_list]

    # Replace the tags
    for tag in tag_list:
        if DATABASE_NAME == "CAPP":
            raw_text = raw_text.replace(tag, "\n")
        elif DATABASE_NAME == "JuriCa":
            raw_text = raw_text.replace(tag, "")
        elif DATABASE_NAME == "Ariane":
            raw_text = raw_text.replace(tag, "")

    return raw_text


def replace_html_entities(raw_text: str):
    """ Replace all the poorly encoded html tags """
    # Define the dictionary of poorly encoded html tags
    dic_html_tags = {"&#128;": "€",
                     "&#149;": "•",
                     "&#156; ": "oe",
                     "&#133;": "...",
                     "&#13;": "",
                     "&#150;": "_",
                     "&lt;": "<",
                     "&gt;": ">",
                     "/spangt;": "",
                     "gt;": "-",
                     "&amp;amp;": "&",
                     "&amp;": "&"
                     }

    # Replace the tags
    res = raw_text
    for html_tag, new_character in dic_html_tags.items():
        res = re.sub(html_tag, new_character, res)

    return res


def replace_unicode_characters(raw_text: str):
    """ Remove the poorly encoded character like \xa0, \x80, etc. """
    # Define the dictionary of poorly encoded html tags
    dic_unicode_tags = {'\xa0': ' ',
                        '\x80': '€',
                        r'(\d\s*)(¿)': r"\1 €",
                        r'\n¿ ': " -"
                        }

    # Replace the tags
    res = raw_text
    for unicode_tag, new_character in dic_unicode_tags.items():
        res = re.sub(unicode_tag, new_character, res)

    return res


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    # Set the directory paths
    input_folder_path = sys.argv[1]
    output_folder_path = sys.argv[2]
    DATABASE_NAME = sys.argv[3]  # "CAPP" #Ariane #CAPP

    # Stops the job if the database name is not yet programmed
    if DATABASE_NAME not in ["CAPP", "JuriCa", "Ariane"]:
        sys.exit("The Database name {} is not recognized ".format(DATABASE_NAME))

    # Stops the job if the input folders does not exist
    if not os.path.isdir(input_folder_path):
        sys.exit("The input folder {} does not exist".format(input_folder_path))

    # Stops the job if the output folders does not exist
    if not os.path.isdir(output_folder_path):
        sys.exit("The output folder {} does not exist".format(output_folder_path))

    # Get the list of xml files
    list_of_xml_files = get_xml_files_from_directory(input_folder_path)

    # Beginning of the extraction
    print("\n##### Text extraction from the folder {} #####\n".format(input_folder_path))

    ## Loop over each xml file of the list
    for xml_file in tqdm(list_of_xml_files):
        try:
            # Get the raw text
            raw_text = get_raw_text_from_xml_file(input_folder_path + xml_file, DATABASE_NAME)
            # Process the text by modifying the xml tags
            processed_text = text_processing(raw_text, DATABASE_NAME)
            # Write the raw text in a .txt file
            outputFile = "{}/{}.txt".format(output_folder_path, xml_file.split(".")[0])
            write_txt_to_file(processed_text, outputFile)
            logging.info("Text of file {} successfully extracted".format(xml_file))

        except Exception:
            logging.exception("Problem extracting the file {}".format(xml_file))

    print("\n##### End ot the extraction of the folder {} #####\n".format(input_folder_path))
    print("##### Files have been written in the folder {} #####".format(output_folder_path))