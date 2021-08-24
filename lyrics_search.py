import re
from bs4.element import ResultSet
import requests
from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict


def web_scraping(url) -> ResultSet:
    """This function searches the html and returns the lyrics"""

    # Fetching html for the Genius page
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in soup("script")]
    lyrics = soup.find_all("div", {"class": "lyrics"})

    return lyrics


def get_works(artist, p, offset):
    """This function searches for artist using parameters provided in p and the offset for pagination"""

    # Fetching artist id for use in musicbrainz API
    response = requests.get("http://musicbrainz.org/ws/2/artist/", params=p)
    dict = response.json()
    # The function exits if no id is found against given artist name
    if len(dict["artists"]) == 0:
        return None
    id = dict["artists"][0]["id"]
    p1 = {"artist": id, "limit": 100, "fmt": "json", "offset": offset}
    # Fetching song list for the given artist
    response2 = requests.get("http://musicbrainz.org/ws/2/work", params=p1)
    dict2 = response2.json()
    return dict2


def song_titles_search(artist, p, offset):
    """This function populates the array with song titles using song data in dictionary for the given artist"""

    # The works are returned as dictionary
    dict2 = get_works(artist, p, offset)
    song_titles = []
    if dict2:
        # We only fetch titles if dictionary is not none
        song_titles += [work["title"] for work in dict2["works"]]
        work_count = dict2["work-count"]
        while len(song_titles) < work_count:
            # Handling pagination to ensure all titles are fetch
            offset += 100
            dict2 = get_works(artist, p, offset)
            song_titles += [work["title"] for work in dict2["works"]]
        return song_titles, work_count
    else:
        # Since the dictionary returned none, therefore, printing error
        print("Invalid entry")
        return None
