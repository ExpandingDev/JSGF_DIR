#!/usr/bin/python3
# Directory JSGF Listing
# Gives a list of filesnames and directories into a JSGF grammer that can be used to navigate using voice control technology
import os, sys, getopt, re

#Default settings
CREATING_FILE = True
TARGET_DIRECTORY = "./"
OUTPUT_FILE = "listing.jsgf"

# Replace common file endings with voice control usable words. Ex: "7z" -> "seven zip"
# TODO: Make this configurable. Nobody wants to go in here and edit it every time.
def convert_part(text):
    text = clean_name(text.lower())
    part_list = (("pdf"), ("jsgf"), ("ods"), ("py"), ("bl"), ("gif"), ("7z", "7zip"), ("mpeg"), ("jpg","jpeg"), ("png"), ("mp3"), ("mp4"), ("wav"), ("gz"), ("txt"), ("docx"), ("odt"), ("tmp"), ("exe"), ("lnk"), ("bz"))
    return_list = ["p. d. f.", "o. d. s.", "pi", "b. l.", "g. i. f.", "seven zip","m. peg","j. peg","p. n. g.","m. p. three","m. p. four", "wave", "g. zip","t. x. t.","doc x.","o. d. t.","temp","e. x. e.","link","b. zip"]
    for index, p in enumerate(part_list):
        if text in p:
            return return_list[index]
    return text

# Separate runalong words, underscores, dashes and numbers that might be in file or directory names
def clean_name(text):

    # Replace spaces, _, [,],(,),_,| with a single space
    text = re.sub(r'[_,\|,\[,\],\(,\)]+'," ",text)

    # Split along changes in capitalization
    text = ' '.join(re.findall('[a-zA-Z][^A-Z]*',text))
    text = text.lower()

    # Add . after single letters to show that each letter must be pronounced Ex. "AI" => "a i" => "a. i."
    text = re.sub(r'(?<!\w)([a-z]{1})(?!\w)',r'\1.',text)

    text = text.replace("0"," zero ")
    text = text.replace("1"," one ")
    text = text.replace("2"," two ")
    text = text.replace("3"," three ")
    text = text.replace("4"," four ")
    text = text.replace("5"," five ")
    text = text.replace("6"," six ")
    text = text.replace("7"," seven ")
    text = text.replace("8"," eight ")
    text = text.replace("9"," nine ")
    text = text.replace("-"," dash ")
    text = text.replace("&"," and ")
    text = text.replace("+"," plus ")
    text = text.replace("@"," at ")
    text = text.replace("%"," percent ")
    text = text.replace("QR", " q. r. ")
    return text

def do_generation():
    #Convert absolute path to reversed domain name format
    absolute_path = os.path.abspath(TARGET_DIRECTORY)
    #Split into an array along the slashes. TODO: Windows support
    tmp_list = re.split("/",absolute_path)
    #Reverse the array
    tmp_list = tmp_list[::-1]
    grammar_name = "root"
    for e in tmp_list:
        grammar_name = grammar_name + "." + e

    #Print out the basic header and the grammar name. [:-1] gets rid of the last "." from the previous for loop
    do_output("#JSGF V1.0;\n\ngrammar " + grammar_name[:-1] + ";\n")

    entries = os.scandir(TARGET_DIRECTORY)
    names = []
    directories = []
    files = []
    for index, entry in enumerate(entries):
        if entry.is_dir():
            directories.append(clean_name(entry.name))
        elif entry.is_file():
            n = entry.name
            s = n.split(".")
            final_name = clean_name(s[0])
            for part in s[1:]:
                final_name = final_name + " dot " + convert_part(part)
            files.append(final_name)

    do_output("public <directories> = (" + (" | ".join(directories)) + ");\n")
    do_output("public <files> = (" + (" | ".join(files)) + ");\n")

# Function that prints out basic usage information
def print_help():
    print("JSGF Directory Listing Script")
    print("Creates a JSGF file that lists filenames and directories present in the targeted directory.")
    print("Useful for filesystem navigation with speech control.")
    print("Usage:")
    print("\tpython3 JSGFLS.py [OPTIONS] DIRECTORY")
    print("")
    print("DIRECTORY = The target directory that the listing will be generated based off of.")
    print("OPTIONS may be:")
    print("\t-h\t--help\t\tDisplays this help text")
    print("\t-n\t--no-file\tDry run. Print out what would be written to the file into")
    print("\t\t\t\tthe console and do not create an output file.")
    print("\t-o\t--output FILE\tSets the name of the file that will be created that contains the listing.")
    print("\t\t\t\t\tDefault: listing.jsgf")
    print("")
    print("Version 1.0")
    print("Author: Tyler Sengia (ExpandingDev)")
    print("tylersengia@gmail.com")

#Grab our args
try:
    opt, args = getopt.getopt(sys.argv,"hno:",["help","no-file","output="])
except getopt.GetoptError: # Malformed arguments/options. Complain and error out
     print_help()
     sys.exit(2)

for option, value in opt:
    if option in ("--output","-o"):
           OUTPUT_FILE = value

#args[1:] is to splice out the first argument, which is the script name
for arg in args[1:]:
    if arg in ("-h", "--help"):
        print_help()
        sys.exit()
    elif arg in ("-n", "--no-file"):
        CREATING_FILE=False

#The JSGF listing file that we create/overwrite. TODO: Windows support
if CREATING_FILE:
    try:
        listing_file = os.open(OUTPUT_FILE,os.O_TRUNC|os.O_CREAT|os.O_WRONLY)
    except:
        print("ERROR: Could not open output file!")
        sys.exit(2)

def do_output(text):
    if not CREATING_FILE:
        print(text)
    else:
        os.write(listing_file,bytes(text.encode()))

do_generation()

#Always remember to close your files kids!
if CREATING_FILE:
    os.close(listing_file)
