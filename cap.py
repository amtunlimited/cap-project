#!/usr/bin/python

import web
import json
import DBA

urls = (
	'/item/', 'item',
	'/', 'index'
)

class item:
	def POST(self):
		ops = json.loads(web.data())
		web.header('Content-Type', 'application/json')
		return json.dumps(DBA.getItem(web.data()))

class index:
	def GET(self):
		index = web.template.frender('index.html')
		return index()

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
