#!/usr/bin/python

import web
import json
import DBA
import datetime

web.config.debug = False

urls = (
	'/item/', 'item',
	'/', 'index',
	'/login/', 'login',
	'/logout/', 'logout',
	'/inventory/', 'inventory',
	'/updateDescription/', 'updateDescription',
	'/updatePrice/', 'updatePrice',
	'/updateCost/', 'updateCost',
	'/updateThreshold/', 'updateThreshold',
	'/updateCount/', 'updateCount',
	'/updateTax/', 'updateTax',
	'/deleteItem/', 'deleteItem',
	'/addItem/', 'addItem',
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'user': 0, 'role':0})

def loggedIn(role):
	if(session.user == 0 or session.role < role):
		raise web.seeother('/login/')

class item:
	def POST(self):
		ops = json.loads(web.data())
		if web.data() == "-1":
			web.header('Content-Type', 'application/json')
			return json.dumps(list(DBA.getAllItems()))
		else:
			web.header('Content-Type', 'application/json')
			return json.dumps(DBA.getItem(web.data()))

class deleteItem:
	def POST(self):
		DBA.removeItem(web.data())

class addItem:
	def POST(self):
		DBA.addItem("", 0, 0, 0, 1, 0)
		raise web.seeother('/')

class updateDescription:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updateDescription(list[0], list[1])

class updatePrice:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updatePrice(list[0], list[1])

class updateCost:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updateCost(list[0], list[1])

class updateThreshold:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updateThreshold(list[0], list[1])

class updateCount:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updateCount(list[0], list[1])

class updateTax:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updateTaxable(list[0], list[1])

class inventory:
	def GET(self):
		#if(session.user!=1):
		#	raise web.seeother('/login/')
		loggedIn(2)

		index = web.template.frender('inventory.html')
		return index()

class index:
	def GET(self):
		#if(session.user!=1):
		#	raise web.seeother('/login/')
		loggedIn(1)

		index = web.template.frender('index.html')
		return index()

class login:
	def GET(self):
		login = web.template.frender('login.html')
		return login()
	
	def POST(self):
		inputs = web.input()
		emp = DBA.getEmployee(inputs.user)
		if(emp == None or inputs.password != emp.Password):
			raise web.seeother('/login/')
		else:
			session.user=emp.EmployeeID
			session.role=emp.Role
			session.loginTime = datetime.datetime.now()
			DBA.addTimeSheetEvent(session.user, datetime.datetime.now(), "ClockIn")
			raise web.seeother('/')
			
class logout:
	def GET(self):
		#session.kill()
		DBA.addTimeSheetEvent(session.user, datetime.datetime.now(), "ClockOut")
		session.user=0
		session.role=1
		raise web.seeother('/login/')

if __name__ == "__main__":
	app.run()
