#!/usr/bin/python

import web
import json
import DBA

web.config.debug = False

urls = (
	'/item/', 'item',
	'/', 'index',
	'/login/', 'login',
	'/logout/', 'logout',
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'user': 0})


class item:
	def POST(self):
		ops = json.loads(web.data())
		web.header('Content-Type', 'application/json')
		return json.dumps(DBA.getItem(web.data()))

class index:
	def GET(self):
		if(session.user==0):
			raise web.seeother('/login/')

		index = web.template.frender('index.html')
		return index()

class login:
	def GET(self):
		login = web.template.frender('login.html')
		return login()
	
	def POST(self):
		if(web.input().user=="root"):
			session.user=1
			raise web.seeother('/')
		else:
			raise web.seeother('/login/')
			
class logout:
	def GET(self):
		session.kill()
		raise web.seeother('/login/')

if __name__ == "__main__":
	app.run()
