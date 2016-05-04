#!/usr/bin/python

import web
import json
import DBA
import datetime
import time

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
	'/checkout/', 'checkout',
	'/employees/', 'employees',
	'/updateName/', 'updateName',
	'/updateRole/', 'updateRole',
	'/updatePassword/', 'updatePassword',
	'/updateHourlyPay/', 'updateHourlyPay',
	'/getEmployee/', 'getEmployee',
	'/deleteEmployee/', 'deleteEmployee',
	'/addEmployee/', 'addEmployee',
	'/settings/', 'settings',
	'/updateSettingValue/', 'updateSettingValue',
	'/getSetting/', 'getSetting',
	'/purchases/', 'purchases',
	'/getPurchase/', 'getPurchase',
	'/getPurchaseItems/', 'getPurchaseItems',
	'/getPurchasesBetween/', 'getPurchasesBetween',
	'/payroll/', 'payroll',
	'/getTimeSheetEvents/', 'getTimeSheetEvents',
	'/getTimeSheetEventsBetween/', 'getTimeSheetEventsBetween',
	'/threshold/', 'threshold',
	'/getThresholdReport/', 'getThresholdReport',
	'/getAllSettings/', 'getAllSettings',
	'/stats/', 'stats',
	'/receipt/', 'receipt',
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'user':0, 'role':0, 'name':""})
render = web.template.render('templates', base='base', globals={'session': session})

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

		#index = web.template.frender('inventory.html')
		#return index()
		return render.inventory()

class index:
	def GET(self):
		#if(session.user!=1):
		#	raise web.seeother('/login/')
		loggedIn(1)

		#index = web.template.frender('index.html')
		#return index()
		return render.index()

class login:
	def GET(self):
		#login = web.template.frender('login.html')
		#return login()
		return render.login()
	
	def POST(self):
		inputs = web.input()
		emp = DBA.getEmployee(inputs.user)
		if(emp == None or inputs.password != emp.Password):
			raise web.seeother('/login/')
		else:
			session.user=emp.EmployeeID
			session.role=emp.Role
			session.name=emp.FirstName
			session.loginTime = int(time.time())
			DBA.addTimeSheetEvent(session.user, int(time.time()), "ClockIn")
			raise web.seeother('/')
			
class logout:
	def GET(self):
		#session.kill()
		DBA.addTimeSheetEvent(session.user, int(time.time()), "ClockOut")
		session.user=0
		session.role=0
		session.name=""
		raise web.seeother('/login/')

class checkout:
	def POST(self):
		loggedIn(1)
		receipt = json.loads(web.data())
		cart = receipt["cart"]

		web.header('Content-type', 'text/plain')
		output = ""

		#output += DBA.getSetting("Name") + "\n"

		total = 0
		tax = 0
		taxrate = receipt["tax"]
		purchaseNum = DBA.addPurchase(session.user, receipt["method"], receipt["discount"], int(time.time()))
		for item in cart:
			DBA.addPurchaseItem(purchaseNum, item["ProductNumber"], item["Count"], item["Price"])
			DBA.incrementCount(item["ProductNumber"], -1*item["Count"])
			output += "{}X{}\n\t{}\n\n".format(item["Description"], item["Count"], item["Price"])
			total += float(item["Price"]) * float(item["Count"])
			tax += float(item["Price"]) * float(item["Count"]) * float(taxrate)

		output += "Subtotal:\t{}\nTax:\t{}\nDiscount:\t{}\n\nTotal\t{}".format(total, tax, receipt["discount"],  total+tax-receipt["discount"])

		return output

class employees:
	def GET(self):
		#if(session.user!=1):
		#	raise web.seeother('/login/')
		loggedIn(1)

		#index = web.template.frender('employees.html')
		#return index()
		return render.employees()

class deleteEmployee:
	def POST(self):
		DBA.removeEmployee(web.data())

class addEmployee:
	def POST(self):
		DBA.addEmployee("", "", 1, "", 0.00)

class getEmployee:
	def POST(self):
		ops = json.loads(web.data())
		if web.data() == "-1":
			web.header('Content-Type', 'application/json')
			return json.dumps(list(DBA.getAllEmployees()))
		else:
			web.header('Content-Type', 'application/json')
			return json.dumps(DBA.getEmployee(web.data()))

class updateName:
	def POST(self):
		str = web.data()
		list = str.split(' ', 2)
		
		DBA.updateEmployeeName(list[0], list[1], list[2])

class updateRole:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updateEmployeeRole(list[0], list[1])

class updatePassword:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updateEmployeePassword(list[0], list[1])

class updateHourlyPay:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.updateEmployeeHourlyPay(list[0], list[1])

class settings:
	def GET(self):
		#if(session.user!=1):
		#	raise web.seeother('/login/')
		loggedIn(1)

		#index = web.template.frender('settings.html')
		#return index()
		return render.settings()

class getAllSettings:
	def POST(self):
		ops = json.loads(web.data())
		
		web.header('Content-Type', 'application/json')
		return json.dumps(list(DBA.getAllSettings()))

class getSetting:
	def POST(self):
		#ops = json.loads(web.data())
		
		web.header('Content-Type', 'application/json')
		return json.dumps(DBA.getSetting(web.data()))

class updateSettingValue:
	def POST(self):
		str = web.data()
		list = str.split(',', 1)
		
		DBA.updateSettingValue(list[0], list[1])

class purchases:
	def GET(self):
		#if(session.user!=1):
		#	raise web.seeother('/login/')
		loggedIn(1)

		#index = web.template.frender('purchases.html')
		#return index()
		return render.purchases()

class getPurchase:
	def POST(self):
		ops = json.loads(web.data())
		if web.data() == "-1":
			web.header('Content-Type', 'application/json')
			return json.dumps(list(DBA.getAllPurchases()))
		else:
			web.header('Content-Type', 'application/json')
			return json.dumps(DBA.getPurchase(web.data()))

class getPurchaseItems:
	def POST(self):
		ops = json.loads(web.data())
		
		web.header('Content-Type', 'application/json')
		return json.dumps(list(DBA.getPurchaseItems(web.data())))

class getPurchasesBetween:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		print(list[0] + "," + list[1])
		
		DBA.getPurchasesBetween(list[0], list[1])

class payroll:
	def GET(self):
		#if(session.user!=1):
		#	raise web.seeother('/login/')
		loggedIn(1)

		#index = web.template.frender('payroll.html')
		#return index()
		return render.payroll()

class getTimeSheetEvents:
	def POST(self):
		web.header('Content-Type', 'application/json')
		return json.dumps(DBA.getTimeSheetEvents())

class getTimeSheetEventsBetween:
	def POST(self):
		str = web.data()
		list = str.split(' ', 1)
		
		DBA.getTimeSheetEventsBetween(list[0], list[1])

class threshold:
	def GET(self):
		#if(session.user!=1):
		#	raise web.seeother('/login/')
		loggedIn(1)

		#index = web.template.frender('threshold.html')
		#return index()
		return render.threshold()

class getThresholdReport:
	def POST(self):
		web.header('Content-Type', 'application/json')
		return json.dumps(list(DBA.thresholdReport()))

class stats:
	def GET(self):
		return render.stats()

class receipt:
	def POST(self):
		loggedIn(1)
		purchase = json.loads(web.data())
		cart = DBA.getPurchaseItems(purchase)

		web.header('Content-type', 'text/plain')
		output = ""

		#output += DBA.getSetting("Name") + "\n"

		total = 0
		tax = 0
		taxrate = 0.06
		for item in cart:
			output += "{}X{}\n\t{}\n\n".format(DBA.getItem(item["ProductNumber"])["Description"], item["Count"], item["Price"])
			total += float(item["Price"]) * float(item["Count"])
			tax += float(item["Price"]) * float(item["Count"]) * float(taxrate)
		
		receipt = DBA.getPurchase(purchase)[0]
		output += "Subtotal:\t{}\nTax:\t{}\nDiscount:\t{}\n\nTotal\t{}".format(total, tax, receipt["Discount"],  total+tax-float(receipt["Discount"]))

		return output


if __name__ == "__main__":
	app.run()
