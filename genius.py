# -*- coding: utf-8 -*-
# SPOTIFY PLAYLIST CSV TO GENIUS LYRIC LINKS
# https://github.com/Suntooth/csv-to-genius
#
# Designed to work with the default output CSVs from Exportify.
# https://exportify.app/
#
# This is the most I've ever commented my code. Hopefully it helps someone!
#
# A note to anyone wishing to contribute:
#   I'd like to avoid regex, even if it makes things more compact or fixes bugs.
#   Regex is difficult to write, difficult to read, and difficult to debug.
#   Find other solutions.
#
# =======================================================================================================

import requests
import csv
from unidecode import unidecode
from string import punctuation

def removePunctuation(inp): # removes characters that aren't in genius urls
    badChars = '''’•●…“”Ææ'''    # already handled by the string module: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    badPhrases = [" - Bonus Track", " - bonus track", " - Hidden Track"]
    toDash = [" - ", "&", "/", "_", ":"]    #turn to a dash instead of being deleted

    inp = inp.replace(" & ", " and ")   # pretty sure the spaces are the difference between this and the cases where it turns to a dash

    # phrase and to-dash replacements MUST be done before the punctuation list. badchars can be anywhere i think
    for phrase in badPhrases:
        inp = inp.replace(phrase, "")

    for dash in toDash:
        inp = inp.replace(dash, "-")

    for punct in punctuation:
        if punct != "-":    # genius keeps dashes in the middle of words (+ this preserves other stuff)
            inp = inp.replace(punct,"")
    
    for char in badChars:  # goes through each character in badChars and removes it from the name
        inp = inp.replace(char,"")
    
    return inp


def removeFeatArtist(inp):    # handles multiple artists
    inp = inp.replace("\,", "@~{a})")   # replace a comma *in an artist name* with something that will not be in the rest of the name...
    artists = inp.split(",", 1)
    artists[0] = artists[0].replace("@~{a})", ",")    # ...in order to bring it back intact after splitting artists
    
    return artists[0]


def removeFeatSong(inp):
    badSuffixes = [" (feat", " [feat", " feat.", " (with", " - Remaster"] # to deal with various forms of suffixes
    parts = [inp]

    for suffix in badSuffixes:
        parts = parts[0].split(suffix, 1)

    return parts[0]
    

lines = []  # will become a 2d array
print("Should the program check if generated links exist?")
check404 = True if int(input("This will greatly increase the time it takes to run. (1 for yes, 2 for no) ")) == 1 else False
print("Running...")

with open("songs.csv", mode="r", newline="", encoding="utf8") as csvfile:   # you have to specify utf8 because otherwise unidecode will break
    start = True
    songs = csv.reader(csvfile) # reads the entire csv file and puts it in a variable

    for row in songs:
        if not start:   # there's headers on the csv file! we need to not read those
            artistNormal = removeFeatArtist(str(row[3]))   # artists is the fourth column in the csv
            artist = unidecode(removePunctuation(removeFeatArtist(str(row[3])))).replace(" ","-") # four functions on one string. lovely
            
            songNormal = str(row[1]) # song title is the second column in the csv
            song = unidecode(removePunctuation(removeFeatSong(str(row[1])))).replace(" ","-")
            
            lines.append([artist,song,artistNormal,songNormal])   # puts all the relevant details in one line of a 2d array
   
        start = False   # for if this was the headers

with open("songs.html", "w", encoding="utf8") as htmlfile:  # writing to a html file is the same as writing to a txt file
    towrite = """<html>
    <head>
        <meta charset="UTF-8">
        <link href="style.css" rel="stylesheet" type="text/css" media="all">
    </head>
    <body>"""   # hashtag justhtmlthings. secret feature: you can use a style.css file to change how the list looks. just for fun

    htmlfile.write(towrite)
    
    for j in range(len(lines)):
        link = 'https://genius.com/' + lines[j][0] + '-' + lines[j][1] + '-lyrics'  # creates the link

# at some point this will have to be changed, since when introducing non-latin characters and consecutive punctuation, things get weird (see Feint, 寻)
        link = link.replace("--", "-")  # to fix double dashes
        link = link.replace("--", "-")  # doing it twice to fix more problems

        if check404:
            if requests.head(link).status_code != 404:  # checking if the song exists on genius
                ahref = '<a href="' + link + '" target="_blank">' + lines[j][2] + ", " + lines[j][3] + """</a><br>
""" # creates the html tag (the line break is to make the source tidier)

            else:   # if it returns a 404 error then add a note in the html file next to that song
                ahref = '<a href="' + link + '" target="_blank">' + lines[j][2] + ", " + lines[j][3] + """</a> (does not exist)<br>
"""
        else:   # if you don't want to check for 404s then it just assumes it exists
            ahref = '<a href="' + link + '" target="_blank">' + lines[j][2] + ", " + lines[j][3] + """</a><br>
"""
        htmlfile.write(ahref)

    towrite = """   </body>
</html>"""

    htmlfile.write(towrite)

print("Done.")
