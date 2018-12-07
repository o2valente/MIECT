#!python
# Example of a cherrypy application that serves static content,
# as well as dynamic content.
#
# JMR@ua.pt 2016
#
# To run:
#	python3 exampleApp.py

import os.path
import cherrypy
import sqlite3
import json
from mixer import mix

# Porta TCP para 10005 (grupo 5)

cherrypy.config.update({'server.socket_port': 10005,})

# The absolute path to this file's base directory:
baseDir = os.path.dirname(os.path.abspath(__file__))

# Dict with the this app's configuration:
config = {
  "/":     { "tools.staticdir.root": baseDir },
  "/js":   { "tools.staticdir.on": True,
             "tools.staticdir.dir": "js" },
  "/css":  { "tools.staticdir.on": True,
             "tools.staticdir.dir": "css" },
  "/html": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "html" },
  "/audio": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "audio" },
  "/images": { "tools.staticdir.on": True,
              "tools.staticdir.dir": "images" },
}


class Root:
    @cherrypy.expose
    def index(self):
       return open("html/index.html").read()

    @cherrypy.expose
    def excertos(self):
       return open("html/excertos.html").read()

    @cherrypy.expose
    def misturador(self):
       return open("html/misturador.html").read()

    @cherrypy.expose
    def songs(self):
       return open("html/songs.html").read()

    @cherrypy.expose
    def list(self, type):
      print(type)
      dataBase = sqlite3.connect('database.db')
   
      if(type == "samples"):
        result = dataBase.execute("SELECT * FROM samples")
        rows = result.fetchall()
        dict = []
        i = 0
        for row in rows:
          dict.append({})
          dict[i]["name"] = row[0]
          dict[i]["date"] = row[1]
          dict[i]["id"] = row[2]
          dict[i]["length"] = row[3]
          dict[i]["uses"] = row[4]
          i = i + 1
        return (json.dumps(dict, indent=4))
      elif(type == "songs"):
        result = dataBase.execute("SELECT * FROM songs")
        rows = result.fetchall()
        dict = []
        i = 0
        for row in rows:
          dict.append({})
          dict[i]["name"] = row[0]
          dict[i]["id"] = row[1]
          dict[i]["length"] = row[2]
          dict[i]["date"] = row[3]
          dict[i]["uses"] = row[4]
          dict[i]["votes"] = row[5]
          dict[i]["author"] = row[6]
          i = i + 1
        return (json.dumps(dict, indent=4))

    @cherrypy.expose
    def get(self, id):
        print(id)
  
        db = sqlite3.connect('database.db')
        samples = db.execute('SELECT * FROM samples WHERE id =?',id)
        if samples : 
          dict = []
          dict.append({})
          dict["name"] = row[0]
          dict["date"] = row[1]
          dict["id"] = row[2]
          dict["length"] = row[3]
          dict["uses"] = row[4]
          return (json.dumps(dict, indent=4))
        else:
          songs = db.execute('SELECT * FROM songs WHERE id =?',id)
          dict = []
          dict.append({})
          dict["name"] = row[0]
          dict["id"] = row[1]
          dict["length"] = row[2]
          dict["date"] = row[3]
          dict["uses"] = row[4]
          dict["votes"] = row[5]
          dict["author"] = row[6]
          return (json.dumps(dict, indent=4))

    @cherrypy.expose
    def sheet(self, sheet):
      mix(sheet)
      
    @cherrypy.expose
    def vote(self, id,points):
      user = cherrypy.request.headers.get('X-Remote-User') #DESCOMENTAR
      #user = "andr.alves" # ELIMINAR LINHA QUANDO O PROJETO TIVER FEITO

      if int(points) == 1 or int(points) == -1: 
        dataBase = sqlite3.connect('database.db')
        c = dataBase.cursor()

        # Averiguar se utilizador já adicionou 'points' à música
        nao_votou = c.execute('SELECT * FROM votos WHERE sid = ? AND email = ? AND points = ?', (id, user, points)).fetchone() is None
        # Se não:
        if nao_votou:

          # Adicionar 'points' à coluna votes da música
          c.execute('''UPDATE songs SET votes = votes + (?)
                  WHERE id = ?''', (points, id,))

          # Averiguar se existia um voto pré-existente em sentido contrário ao que se quer fazer agora
          not_points = int(points) * -1
          rem_voto = c.execute('SELECT * FROM votos WHERE sid = ? AND email = ? AND points = ?', (id, user, not_points)).fetchone() is None
          
          # Eliminar, se existir, o voto pré-existente em sentido contrário ao que se quer fazer agora
          c.execute('DELETE FROM votos WHERE email = ? AND sid = ? AND points = ?', (user, id, not_points))
        
          # Se não havia um voto contrário, adicionar o novo voto
          if rem_voto:
            # Guardar voto na tabela votos
            c.execute('''INSERT INTO votos (email, sid, points) 
              VALUES (?, ?, ?)''', (user, id, points,))
          
          dataBase.commit()
          c.close()


cherrypy.quickstart(Root(), "/", config)