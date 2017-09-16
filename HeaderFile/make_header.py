#!/usr/bin/python

from time import strftime
import platform, sys, os

LINUX = "Linux"
WINDOWS = "Windows"

def create_header(title):
    # Convert all letters to lower case.
    title = title.lower()

    # Remove spaces from the title.
    title = title.replace(' ', '_')

    descrpt = raw_input("Enter a description: ")
    if descrpt == "stop":
        exit(1)

    name = "Cloquet Alban"# raw_input("Enter your name: ")
    ver = "Python 3.6" # raw_input("Enter the version number: ")
    div = '======================================='

    # Create a file that can be written to.
    try:
        original = open(title, 'r')
        data = original.read()
        original.close()
    except IOError:
        data = ""
        pass

    filename = open(title, 'w+')

    # Set the date automatically.
    date = strftime("%Y/%m/%d")

    date.format()
    # Write the data to the file.
    filename.write('#!/usr/bin/env python3')
    filename.write('\n# title\t\t\t\t: ' + title)
    filename.write('\n# description\t\t: ' + descrpt)
    filename.write('\n# author\t\t\t: ' + name)
    filename.write('\n# date\t\t\t\t: ' + date)
    filename.write('\n# version\t\t\t: ' + ver)
    filename.write('\n# usage\t\t\t\t: ' + 'python ' + title)
    filename.write('\n# notes\t\t\t\t: ')
    filename.write('\n# python_version\t: 3.6')
    filename.write('\n# ' + div * 2 + '\n')
    filename.write('\n# Import the modules needed to run the script.')
    filename.write('\n')
    filename.write('\n')

    # Write all data of the file
    filename.write(data)

    # Close the file after writing to it.
    filename.close()

    # Clear the screen. This line of code will not work on Windows.
    if platform.system() == WINDOWS:
        os.system("cls")
    elif platform.system() == LINUX:
        os.system("clear")

if len(sys.argv) == 1:
    title = raw_input('Enter a title for your script: ')
    # Add .py to the end of the script.
    title = title + '.py'
    create_header(title)

else:
    l_File = "make_header.py"
    for title in sys.argv:
        if title[len(title) - len(l_File):] == l_File:
            continue

        create_header(title)
