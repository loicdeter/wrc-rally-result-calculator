import sqlite3
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

conn = sqlite3.connect(config['settings']['database'])
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS resultats (id INTEGER PRIMARY KEY, categorie TEXT, rally INTEGER, pseudo TEXT, nom TEXT, vehicule TEXT, tempsFinal TEXT, tempsPowerStage TEXT, pointsCategorie INTEGER, pointsPowerStage INTEGER, pointsGlobal INTEGER)''')

def FindResult(categorie, rally, pseudo):
    c.execute('SELECT * FROM resultats WHERE categorie = ? AND rally = ? AND pseudo = ?', (categorie, rally, pseudo))
    return c.fetchone()

def GetRallyResults(rally):
    c.execute('SELECT * FROM resultats WHERE rally = ?', (rally,))
    return c.fetchall()

def InsertResult(categorie, rally, pseudo, nom, vehicule, tempsFinal, tempsPowerStage, pointsCategorie, pointsPowerStage, pointsGlobal):
    c.execute('INSERT INTO resultats (categorie, rally, pseudo, nom, vehicule, tempsFinal, tempsPowerStage, pointsCategorie, pointsPowerStage, pointsGlobal) VALUES (?,?,?,?,?,?,?,?,?,?)', (categorie, rally, pseudo, nom, vehicule, tempsFinal, tempsPowerStage, pointsCategorie, pointsPowerStage, pointsGlobal))
    conn.commit()