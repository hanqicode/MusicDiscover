from googlesearch import search
import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import time

"""
3. Search on the Internet with the identifiers(song name and singer name);
4. Parse and get the composer and arranger;
5. Save composer and arranger into database;
"""
# read songs from database
db = mysql.connector.connect(user='root', password='19921230', database='music_discover')
reader = db.cursor(buffered=True)
writer = db.cursor()
readSql = "SELECT * " + \
          "FROM LibraryMusic " + \
          "WHERE isValid=1;"
writeSql = "Update LibraryMusic " + \
           "SET composer=%s, arranger=%s, isValid=%s " + \
           "WHERE songName=%s and singer=%s;"
reader.execute(readSql)

for row in reader:
    time.sleep(30)
    songName = row[0]
    singer = row[1]
    writeData = [None, None, "0", songName, singer]

    # search songName + singer and get baike pages
    query = "歌曲 " + songName + " " + singer
    print("[Debug] " + query + " querying...")
    queryResult = []
    for link in search(query,  # The query typed in Google search
                       tld='com',  # The top level domain
                       lang='en',  # The language
                       num=10,  # Number of results per page
                       start=0,  # First result to retrieve
                       stop=10,  # Last result to retrieve
                       pause=2.0,  # Lapse between HTTP requests
                       ):
        if "baike.baidu.com" in link:
            queryResult.append(link)

    if not queryResult:
        print("  [Warn] Cannot find baike page for query: " + query)
        writer.execute(writeSql, writeData)
        db.commit()
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

    # update song database
    for key, value in basicInfoDic.items():
        if key == "谱曲" or key == "作曲":
            writeData[0] = value
        elif key == "编曲":
            writeData[1] = value

    print("  [Debug] composer: " + str(writeData[0]) + ", arranger: " + str(writeData[1]))
    print("  [Debug] write data: " + str(writeData))
    writer.execute(writeSql, writeData)
    db.commit()

writer.close()
reader.close()
db.close()
print("[Info] Completed! Get the song database:")
# do not delete me
