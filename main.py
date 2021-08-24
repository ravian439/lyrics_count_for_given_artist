import re
import requests
from requests.structures import CaseInsensitiveDict
from lyrics_search import song_titles_search, web_scraping


def main():
    # Getting artist name from user and initializing key variables
    artist = input("Enter artist name: ")
    p = {"query": "artist:" + artist, "fmt": "json"}
    offset = 0
    total_word_count = 0

    song_titles, work_count = song_titles_search(artist, p, offset)

    for title in song_titles:
        # Lyrics fetched for each title entry
        song_title = title
        token = "icEFjpvny8JSYQMtOenYt7CHrQO5B10ZEAZ4fHUiVMYdy45cdFVf8FHEgGvaDWch"
        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Bearer " + token
        params = {"q": song_title}
        reqres = requests.get(
            "https://api.genius.com/search", params=params, headers=headers
        )
        dict3 = reqres.json()
        # Getting url for the searched song
        url_extract = dict3["response"]["hits"][0]["result"]["url"]
        lyr = list(web_scraping(url_extract))
        while len(lyr) == 0:
            lyr = list(web_scraping(url_extract))
        lyrics_final = ""

        if len(lyr) > 0:
            # Cleaning the string by removing unnecessary html tags
            lyrics_final = re.sub("<.*>", "", str(lyr[0]))
            lyrics_final = re.sub("\[.*\n", "", lyrics_final)
            lyrics_final = re.sub("<(.|\n)*>", "", lyrics_final)

        count_words = len(lyrics_final.split())
        # Summation of word count for all songs
        total_word_count += count_words

    print(
        "The average word count for this artist's work is "
        + str(total_word_count / work_count)
    )


if __name__ == "__main__":
    main()
