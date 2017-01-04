import sqlite3 as s
import pyperclip

conn = s.connect('gotDB.bytes')
c = conn.cursor()
c.execute("SELECT character_id FROM XXGOT_CHAPTER_CHARACTERS")
rows = c.fetchall()

noRows = 0

for row in list(set(rows)):
    if not str(row[0]).isdigit():
        newName = row[0]
        print(newName)
        pyperclip.copy(newName)
        noRows += 1
        c.execute("INSERT INTO xxgot_characters (name) VALUES ('{0}')".format(newName))
        c.execute("SELECT max(id) FROM xxgot_characters")
        idRow = c.fetchone()[0]
        shortDesc = input('0 if it exists - enter short description > ')
        if shortDesc != 0:
            c.execute("INSERT INTO xxgot_characters_tl (character_id, language, short_desc) VALUES (?,'English',?)",(idRow, shortDesc))
        c.execute("UPDATE xxgot_chapter_characters SET character_id = ? WHERE character_id = ?",(idRow,newName))
        conn.commit()


print(noRows)
conn.close()
