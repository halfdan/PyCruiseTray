import sqlite3
import os

class ServerManager:
    def __init__(self):
	path = os.getenv('HOME')
	self.conn = sqlite3.connect('%s/.pycruisetray.db' % path)
	self.cursor = self.conn.cursor()
	self.create_database()

    def create_database(self):
	self.cursor.execute('create table if not exists servers (id INTEGER PRIMARY KEY, name TEXT, url TEXT)')
	self.conn.commit()

    def add(self, name, url):
	self.cursor.execute('insert into servers (name, url) values (?, ?)', (name, url))
	self.conn.commit()

    def remove(self, name):
	self.cursor.execute('delete from servers where name = "?"', name)
	self.conn.commit()

    def list(self):
	rows = self.cursor.execute('select id, name, url from servers')
	servers=[]
	for row in rows:
	    servers.append({
		'id': row[0],
		'name': row[1],
		'url': row[2]
	    })
	return servers
		
