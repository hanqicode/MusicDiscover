from bs4 import BeautifulSoup
from googlesearch import search
import urllib.request
import itertools

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

print("[Info] Start to discover your music...")
"""
1. Parse Youtube Music Library into a dictionary with song name and singer name;
"""
# parse Youtube Music page
soup = BeautifulSoup(open("/Users/qihan/Documents/Workplace/Python/Temp/musicDiscover/page.html"), "html.parser")
rawSongs = soup.find_all("div", {"class": "flex-columns style-scope ytmusic-responsive-list-item-renderer"})
# for each rawSong:
#     index 1: song name
#     index 5: singer and album

songDic = {}

# parse to get song + singer
for rawSong in rawSongs:
    songName = rawSong.contents[1].contents[1].contents[0].contents[0]
    singer = None
    singerTemp = rawSong.contents[5].contents[1].contents[0]  # in case some singers are not a single person
    if isinstance(singerTemp, str):
        singer = singerTemp
    else:
        singer = singerTemp.contents[0]

    songDic[songName] = singer

print("[Info] Step 1 completed! Get the song dictionary:")
print("[Info] " + str(songDic))

# TODO: Need to delete after debugging!
songDic = dict(itertools.islice(songDic.items(), 4))
print("[Debug] for debugging: " + str(songDic))

"""
2. Search on the Internet with the identifiers(song name and singer name);
"""
songDatabase = {}  # {songName : {singer:Jay, composer: Jay, arranger: Jay}}

for song, singer in songDic.items():
    # search song + singer and get baike pages
    query = song + " " + singer
    print("[Debug] " + query + " querying...")
    queryResult = []
    for link in search(query,  # The query typed in Google search
                       tld='com',  # The top level domain
                       lang='en',  # The language
                       num=10,  # Number of results per page
                       start=0,  # First result to retrieve
                       stop=20,  # Last result to retrieve
                       pause=2.0,  # Lapse between HTTP requests
                       ):
        if "baike.baidu.com" in link:
            queryResult.append(link)

    if not queryResult:
        print("[Warn] Cannot find baike page for query: " + query)
        continue

    # parse baike page
    baikePage = queryResult[0]
    baikePageSourceCode = urllib.request.urlopen(baikePage).read()
    baikePageHtml = BeautifulSoup(baikePageSourceCode, 'html.parser')

    # get composer and arranger from baike page
    basicInfoNameList = baikePageHtml.find_all("dt", {"class": "basicInfo-item name"})
    basicInfoValueList = baikePageHtml.find_all("dd", {"class": "basicInfo-item value"})
    basicInfoDic = {}
    for i in range(len(basicInfoNameList)):
        name = basicInfoNameList[i].contents[0]
        name = name.strip('\n')
        name = name.replace(u'\xa0', u'')

        valueTemp = basicInfoValueList[i].contents
        value = None
        if valueTemp[0] != '\n':
            value = valueTemp[0]
        else:
            value = valueTemp[1].contents[0]
        value = value.strip('\n')

        basicInfoDic[name] = value

    # print("[Debug] " + query + ": " + str(basicInfoDic))
    # update song database
    songDatabase[song] = {}
    songDatabase[song]["singer"] = singer

    for key, value in basicInfoDic.items():
        if key == "谱曲":
            songDatabase[song]["composer"] = value
        elif key == "编曲":
            songDatabase[song]["arranger"] = value

print("[Info] Step 2 completed! Get the song database:")
print("[Info] " + str(songDatabase))
# [Info] {'原来你什么都不要': {'singer': '孙燕姿', 'composer': '郭子', 'arranger': 'Terence Teo'}, '一生中最爱 (电影《双城故事》歌曲)': {'singer': '谭咏麟', 'composer': '伍思凯', 'arranger': '卢东尼'}, '死性不改': {'singer': "Boy'z", 'composer': '张佳添'}}
# do not delete me
