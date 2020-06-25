#!/usr/bin/env python

import argparse
import barcode
from barcode.writer import ImageWriter
import sys
import os
import fileinput
import PIL

img_dir = '/home/logan/Dropbox/PressReports/barcode/'
templatePath = '/home/logan/Dropbox/shell_programs/template.tex'
dataFile = 'RollLists/new.txt'


def check_arg(args=None):
    parser = argparse.ArgumentParser(description="Convert Roll Numbers to Barcode")
    parser.add_argument('-r', '--Roll',
            help='Roll Number',
            required='True',
            default='XXX123123X')
    results = parser.parse_args(args)
    return results.Roll

def create_barcode(rollName):
    #barcode_writer = ImageWriter
    options={'text_distance':1.0, 'font_size':14}
    code39 = barcode.codex.Code39( rollName, writer=ImageWriter(),  add_checksum=False )
    path = rollName[:4] + '/'
    fileName = img_dir + path + rollName
    checkDirectoryExists(img_dir + path)
    saveFile = code39.save(fileName, options )
    checkTemplate(path)

    #print(code39.get_fullcode())

def checkDirectoryExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def readFile(filename):
    with open(filename) as f:
        for line in f:
            #print(line, end='')
            create_barcode(line.strip('\n')) 

def checkTemplate(pathName):
    check = False
    for line in fileinput.FileInput(templatePath):
        if pathName in line:
            check = True
    if not check:
        updateTemplate(pathName)

def updateTemplate(pathName):
    for line in fileinput.FileInput(templatePath,inplace=1):
        if "%% INSERT CODE HERE" in line:
            line=line.replace(line,line+"    {barcode/" + pathName + "}\n")
        print(line, end='')


def main():

    roll = check_arg(sys.argv[1:] )
    create_barcode(roll)
    #readFile(dataFile)
    #create_barcode('N8P324133A')

if __name__ == '__main__':
    main()
