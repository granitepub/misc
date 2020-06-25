#!/usr/bin/python

# This program is the same as webScrap3 but uses urllib3 instead of urllib
from bs4 import BeautifulSoup as soup
import urllib3
import unicodedata
from enum import Enum

## Notes --
## To get items in an html table:
 #  -- First find the table or tables
 #  -- Loop throug tables to isolate a table at a time
 #  -- Find all the tr's (table rows )for table.
 #  -- Then find all td's (table data) for tr's.
 #  -- Below I find all the a tags for td, then get the text of the title text for the a tags.
 #  -- Next I get the the title text of the td tags
 #  -- Next split the title into 2 parts splitting on the ':' char.
 #  -- put all this into a tuple and add it to the list names.


names = []

def getData(url_file):
    description = {}

    sauce = soup(open(url_file), "html.parser")
    data = sauce.findAll('table',{'class':'wikitable nounderlines'})

    for table in data:
        for row in table.find_all('tr'):
            for t in row.find_all('td'):
                #print(t.get('title'))
                if t.get('title'):
                    #print(t.get('title'), t.find('a').get('title'))
                    names.append((t.find('a').get('title'), t.get('title').split(':')[1], t.get('title').split(':')[0]))
                    #names.append((t.get('title').split(':')[1].lstrip(), t.find('a').get('title')[0]))



    for a, b, c in names:
        if len(a) == 1 and a != False :
            print(a, b + ';', c)

def main():
    url_file = 'Emoji.html'
    getData(url_file)

if __name__ == '__main__':
    main()



