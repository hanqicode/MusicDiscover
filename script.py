"""
# Music Discover by Qi

## Motivation:
To dig out more music, I would parse my current library songs into three categories:
    1. singer
    2. composer
    3. arranger
Then find out all music made by those people.

## Action Items
1. Parse Youtube Music Library into a dictionary with song name and singer name;
2. Search on the Internet with the identifiers(song name and singer name);
3. Parse and get the composer and arranger
4. Search on the Internet for songs with singers, composers and arrangers;
5. Listen and find out what you like;
"""

from bs4 import BeautifulSoup

"""
1. Parse Youtube Music Library into a dictionary with song name and singer name;
"""
soup = BeautifulSoup(open("/Users/qihan/Documents/Workplace/Python/Temp/parseYoutubeMusic/page.html"), "html.parser")
rawSongs = soup.find_all("div", {"class": "flex-columns style-scope ytmusic-responsive-list-item-renderer"})
# for each rawSong:
#     index 1: song name
#     index 5: singer and album

songDic = {}

for rawSong in rawSongs:
    songName = rawSong.contents[1].contents[1].contents[0].contents[0]
    singer = None
    singerTemp = rawSong.contents[5].contents[1].contents[0]  # in case some singers are not a single person
    if isinstance(singerTemp, str):
        singer = singerTemp
    else:
        singer = singerTemp.contents[0]

    songDic[songName] = singer

"""
2. Search on the Internet with the identifiers(song name and singer name);
"""
# do not delete me
