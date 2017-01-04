import sqlite3 as s
import requests
from bs4 import BeautifulSoup
import time


startChapter = 19
endChapter = 74

conn = s.connect('gotDB.bytes')
c = conn.cursor()
c.execute("SELECT id,name FROM XXGOT_CHARACTERS")
rows = c.fetchall()


startURL = 'http://towerofthehand.com/books/101/0'
endURL = '/index.html'

for i in range(startChapter, endChapter):
    url = startURL + str(i) + endURL

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Extract Chapter Number
    mystr = soup.select('div#breadbox > div#crumbs > a')[1].text
    chapterNo = [int(s) for s in mystr.split() if s.isdigit()][0]
    print('Chapter #' + str(chapterNo))
    # Extract Characters
    for name in soup.select('div#appearances > ol > li > a'):
        foundName = name.text
        for dbName in rows:
            if dbName[1] == name.text:
                foundName = dbName[0]
        c.execute(
            "INSERT INTO XXGOT_CHAPTER_CHARACTERS "
            "(chapter_id, character_id, main_character) VALUES "
            "({0},'{1}',1)".format(chapterNo, foundName))
        print(
            "INSERT INTO XXGOT_CHAPTER_CHARACTERS "
            "(chapter_id, character_id, main_character) VALUES "
            "({0},'{1}',1)".format(chapterNo, foundName))
    time.sleep(3)
    print()

conn.commit()
conn.close()
