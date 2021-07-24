from bs4 import BeautifulSoup
import mysql.connector

"""
1. Parse Youtube Music Library into a dictionary with song name and singer name;
2. Save song name and singer name into database;
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

# save into database
db = mysql.connector.connect(user='root', password='your_password', database='music_discover')
cursor = db.cursor()

sql = "INSERT INTO LibraryMusic " + \
      "(songName, singer, isValid) " + \
      "VALUES (%s, %s, 1);"

for key, value in songDic.items():
    data = [key, value]
    cursor.execute(sql, data)

db.commit()
cursor.close()
db.close()
# do not delete me
