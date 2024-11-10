# CSV to Genius
 Converts a CSV of a Spotify playlist to a HTML file containing a list of links to the lyrics of each song, with the option to check if each link exists.

## Limitations
- Cannot currently handle non-Latin scripts (e.g. Japanese, Cyrillic, Tifinagh).
- Checking if links exist takes a long time compared to not checking - 34.808 seconds vs 0.012 seconds for the same 100-song playlist. (This is why there is an option to not check links.)
- There will always be some songs where the Genius page can't be found with just the information on Spotify, usually due to artists changing names or the Genius page having a slightly different song name to Spotify.

## Known issues
- Repeated consecutive punctuation may be processed incorrectly.
- Links may be processed incorrectly if the artist and/or song name contains punctuation that isn't explicitly handled.
- Some cases (features, subtitles, etc.) may not be handled in the same way that Genius handles them, causing the link to lead to a 404 error even if the song exists on Genius.
- If a song has a Genius page but is missing lyrics, it will still show as not existing.

## Instructions
### Installation
#### Option 1 (may be outdated)
Download `csv-to-genius.exe` from [the latest release](https://github.com/suntooth/csv-to-genius/releases/latest).

#### Option 2 (guaranteed to be up-to-date)
Ensure you have the packages `string`, `requests`, `csv`, and `unidecode` installed, as well as Python 3.10.8, then download the source code. Other versions of Python may work, but may not.

### Usage
1. Export the playlist you want to process using [Exportify](https://exportify.app/). Other services that export a CSV with the exact same format will also work.
2. Rename the CSV file to `songs.csv`.
3. Place `songs.csv` and this program in the same folder.
4. Run `csv-to-genius.exe` (option 1) or `genius.py` (option 2). It will create a file named `songs.html` with the list of links.
