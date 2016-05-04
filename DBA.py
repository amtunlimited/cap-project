import web

db = web.database(dbn = 'sqlite', db = 'cap.db')

#add a new item to inventory
def addItem(description, price, count, threshold, taxable, cost):
	db.insert('Inventory', Description=description, Price=price, Count=count, Threshold=threshold, Taxable=taxable, Cost=cost)

#remove item with given productNumber from inventory
def removeItem(productNumber):
	db.delete('Inventory', where='ProductNumber=$productNumber', vars=locals())

#get the item from inventory with the given product number
def getItem(productNumber):
	try:
		return db.select('Inventory', where='ProductNumber=$productNumber', vars=locals())[0]
	except IndexError:
		return None

#get all items from inventory, ordered by product number
def getAllItems():
	return db.select('Inventory', order = 'ProductNumber')

#update description for item
def updateDescription(productNumber, description):
	db.update('Inventory', where='ProductNumber=$productNumber', vars=locals(), Description=description)

#update Price for item
def updatePrice(productNumber, price):
	db.update('Inventory', where='ProductNumber=$productNumber', vars=locals(), Price=price)

#update Cost for item
def updateCost(productNumber, cost):
	db.update('Inventory', where='ProductNumber=$productNumber', vars=locals(), Cost=cost)

#update Threshold for item
def updateThreshold(productNumber, threshold):
	db.update('Inventory', where='ProductNumber=$productNumber', vars=locals(), Threshold=threshold)

#update Count for item
def updateCount(productNumber, count):
	db.update('Inventory', where='ProductNumber=$productNumber', vars=locals(), Count=count)

#update Taxable for item
def updateTaxable(productNumber, taxable):
	db.update('Inventory', where='ProductNumber=$productNumber', vars=locals(), Taxable=taxable)

#increment (or decrement with negative delta) item's count field
def incrementCount(productNumber, delta):
	db.query(
		'UPDATE Inventory \
		SET count = count + $delta \
		WHERE ProductNumber = $productNumber',
		vars=locals()
	)

#add a new user
def addEmployee(firstName, lastName, role, password, hourlyPay):
	db.insert('Employee', FirstName = firstName, LastName = lastName, Role = role, Password = password, HourlyPay = hourlyPay)

#get the employee with the given ID, returning None if not found	
def getEmployee(employeeID):
	try:
		return db.select('Employee', where='EmployeeID=$employeeID', vars=locals())[0]
	except IndexError:
		return None

#get all Employees, ordered by Employee ID
def getAllEmployees():
	return db.select('Employee', order = 'EmployeeID')

#remove employee with specified employeeID
def removeEmployee(employeeID):
	db.delete('Employee', where='EmployeeID=$employeeID', vars=locals())

#update Name for Employee
def updateEmployeeName(employeeID, firstName, lastName):
	db.update('Employee', where='EmployeeID=$employeeID', vars=locals(), FirstName=firstName, lastName=lastName)

#update Role for Employee	
def updateEmployeeRole(employeeID, role):
	db.update('Employee', where='EmployeeID=$employeeID', vars=locals(), Role=role)
	
#update Password for Employee
def updateEmployeePassword(employeeID, password):
	db.update('Employee', where='EmployeeID=$employeeID', vars=locals(), Password=password)

#update HourlyPay for Employee
def updateEmployeeHourlyPay(employeeID, hourlyPay):
	db.update('Employee', where='EmployeeID=$employeeID', vars=locals(), HourlyPay=hourlyPay)

#create new TimeSheet event
def addTimeSheetEvent(employeeID, timeStamp, eventType):
	db.insert('TimeSheet', EmployeeID=employeeID, TimeStamp=timeStamp, Type=eventType)

#Get all TimeSheetEvents from TimeSheet table
def getAllTimeSheetEvents():
	return db.select('TimeSheet', order = 'EventID')

#Get all TimeSheetEvents that took place between beginTime and endTime
def getTimeSheetEventsBetween(beginTime, endTime):
	return db.select('TimeSheet', where='TimeStamp > $beginTime AND TimeStamp < $endTime', order = 'EventID')

#get setting with given settingID, returning None if not found
def getSetting(settingID):
	try:
		return db.select('Setting', where='SettingID=$settingID', vars=locals())[0]
	except IndexError:
		return None

#Get all settings from setting table
def getAllSettings():
	return db.select('Setting', order = 'SettingID')

#set the value for the setting with the given settingID
def updateSettingValue(settingID, settingValue):
	db.update('Setting', where='SettingID=$settingID', vars=locals(), SettingValue=settingValue)

#add new Purchase into Purchase table
def addPurchase(employeeID, paymentMethod, discount, TimeStamp):
	return db.insert('Purchase', EmployeeID=employeeID, PaymentMethod=paymentMethod, Discount=discount, TimeStamp=TimeStamp)

#add new PurchaseItem
def addPurchaseItem(purchaseNumber, productNumber, count, price):
	return db.insert('PurchaseItem', PurchaseNumber=purchaseNumber, ProductNumber=productNumber, Count=count, Price=price)
	
#Return items where Count <= Threshold
def thresholdReport():
	return db.select('Inventory', where='Count <= Threshold')

#Get purchase with given PurchaseNumber
def getPurchase(purchaseNumber):
	return db.select('Purchase', where='PurchaseNumber=$purchaseNumber', vars=locals())

#Get all purchases from Purchase table
def getAllPurchases():
	return db.select('Purchase', order = 'PurchaseNumber')

#Get all purchases that took place between beginTime and endTime
def getPurchasesBetween(beginTime, endTime):
	return db.select('Purchase', where='TimeStamp > $beginTime AND TimeStamp < $endTime', order = 'PurchaseNumber')

#Get all items purchased in the transaction with given purchaseNumber
def getPurchaseItems(purchaseNumber):
	return db.select('PurchaseItem', where= 'PurchaseNumber = $purchaseNumber', order = 'PurchaseLineID', vars=locals())
	
