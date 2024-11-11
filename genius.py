# -*- coding: utf-8 -*-
# SPOTIFY PLAYLIST CSV TO GENIUS LYRIC LINKS
# https://github.com/Suntooth/csv-to-genius
#
# Designed to work with the default output CSVs from Exportify
# https://exportify.app/
#
# This is the most I've ever commented my code. Hopefully it helps someone!
#
# ========================================================================================

import requests
import csv
from unidecode import unidecode
from string import punctuation

def removePunctuation(inp): # removes characters that aren't in genius urls
    badChars = '''’•●…“”Ææ'''    # already handled by the string module: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

# this series of replacements could probably be done in a more compact way, but i'd rather keep it clear what's what
    inp = inp.replace(" - Bonus Track", "") # in most cases this is how genius does it
    inp = inp.replace(" - bonus track", "")
    inp = inp.replace(" - Hidden Track", "")
    inp = inp.replace(" & ", "and")   # inconsistent! sometimes it's just removed like other punctuation. hopefully the spaces are the difference
    inp = inp.replace("&", "-") # U&ME by alt-j was the realisation here
    inp = inp.replace(" - ", "-")   # if this causes double dashes it'll usually be fixed later
    inp = inp.replace("/", "-")

    for punct in punctuation:
        if punct != "-":    # genius keeps dashes in the middle of words (+ this preserves other stuff)
            inp = inp.replace(punct,"")
    
    for i in badChars:
        inp = inp.replace(i,"")
    
    return inp


def removeFeatArtist(inp):    # handles multiple artists
    inp = inp.replace("\,", "@~{a})")   # replace a comma *in an artist name* with something that will not be in the rest of the name...
    artists = inp.split(",", 1)
    artists[0] = artists[0].replace("@~{a})", ",")    # ...in order to bring it back intact after splitting artists
    return artists[0]

def removeFeatSong(inp):
# same as the above replacements. this function could be more compact but this way of doing it is much clearer
    parts = inp.split("(feat", 1)   # removes "(feat. [artist])" and "(featuring [artist])"
    parts = parts[0].split("(with", 1)
    parts = parts[0].split("[feat", 1)
    parts = parts[0].split(" feat.", 1)  # there's a few songs that don't use brackets for features
    parts = parts[0].split(" - Remaster")   # i can't account for most remasters without regex but i can do this variant
    return parts[0]
    

lines = []  # will be a 2d array later on
check404 = True if int(input("""Should the program check if generated links exist?
This will greatly increase the time it takes to run. (1 for yes, 2 for no) """)) == 1 else False    # 34.808 seconds vs 0.012 seconds
print("Running...")                                                                                 # for the same 100-song playlist

with open("songs.csv", mode="r", newline="", encoding="utf8") as csvfile:   # reading the csv file
    start = True
    songs = csv.reader(csvfile) # initialise the csv reader

    for row in songs:
        if not start:   # there's headers on the csv file! we need to not read those
            artistNormal = removeFeatArtist(str(row[3]))   # artists is the fourth column in the csv
            artist = unidecode(removePunctuation(removeFeatArtist(str(row[3])))).replace(" ","-") # four functions on one string. lovely
            
            songNormal = str(row[1]) # song title is the second column in the csv
            song = unidecode(removePunctuation(removeFeatSong(str(row[1])))).replace(" ","-")
            
            lines.append([artist,song,artistNormal,songNormal])   # puts all the relevant details in one line of a 2d array
   
        start = False   # for if this was the headers

with open("songs.html", "w", encoding="utf8") as htmlfile:  # writing to a html file
    towrite = """<html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>"""   # hashtag justhtmlthings

    htmlfile.write(towrite)
    
    for j in range(len(lines)):
        link = 'https://genius.com/' + lines[j][0] + '-' + lines[j][1] + '-lyrics'  # creates the link

        link = link.replace("--", "-")  # to fix anywhere there might be weirdness with punctuation
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

    towrite = """</body>
</html>"""

    htmlfile.write(towrite)

print("Done.")
