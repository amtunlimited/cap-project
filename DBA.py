import web

db = web.database(dbn = 'sqlite', db = 'CAP')

#add a new item to inventory
def addItem(productNumber, description, price, count, threshold, taxable, cost):
	db.insert('Inventory', ProductNumber=productNumber, Description=description, Price=price, Count=count, Threshold=threshold, Taxable=taxable, Cost=cost)

#get the item with the given product number
def getItem(productNumber):
	try:
		return db.select('Inventory', where='ProductNumber=$productNumber')[0]
	except IndexError:
		return None

#update count field server-side		
def updateCount(productNumber, delta):
	db.query(
		'UPDATE Inventory \
		SET count = count + $delta \
		WHERE ProductNumber = $productNumber',
		vars={productNumber = productNumber, delta = delta}
	)
	
