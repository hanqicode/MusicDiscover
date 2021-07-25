import mysql.connector

libraryMusicDatabase = mysql.connector.connect(user='root', password='your_password', database='music_discover')
composerReader = libraryMusicDatabase.cursor(buffered=True)
composerSql = "SELECT DISTINCT composer " \
          "FROM LibraryMusic;"
composerReader.execute(composerSql)

composers = []

for composer in composerReader:
    composers.append(composer[0])

# print(composers)

arrangerReader = libraryMusicDatabase.cursor(buffered=True)
arrangerSql = "SELECT DISTINCT arranger " \
          "FROM LibraryMusic;"
arrangerReader.execute(arrangerSql)

arrangers = []

for arranger in arrangerReader:
    arrangers.append(arranger[0])

# print(arrangers)

people = {"None"}
for composer in composers:
    people.add(composer)

for arranger in arrangers:
    people.add(arranger)

print(people)
print(len(composers))
print(len(arrangers))
print(len(people))
composerReader.close()
arrangerReader.close()

peopleDatabase = mysql.connector.connect(user='root', password='your_password', database='music_discover')
writer = peopleDatabase.cursor()
writeSql = "INSERT INTO ComposerAndArranger " \
           "(person, isValid) VALUES (%s, %s);"

temp = []

for person in people:
    if person == "None" or person in temp or person is None:
        continue

    temp.append(person)
    writeData = [person, '1']
    writer.execute(writeSql, writeData)
    peopleDatabase.commit()

writer.close()
peopleDatabase.close()
