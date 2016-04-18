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
def addEmployee(employeeID, firstName, lastName, role):
	db.insert('Employee', EmployeeID = employeeID, FirstName = firstName, LastName = lastName, Role = role)

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

#create new TimeSheet event
def addTimeSheetEvent(employeeID, timeStamp, eventType):
	db.insert('TimeSheet', EmployeeID=employeeID, TimeStamp=timeStamp, Type=eventType)
