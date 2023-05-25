import mysqlx
from mysqlx.errors import DatabaseError
# Connect to server on localhost, close session also defined here

session = mysqlx.get_session({
    'host': 'localhost',
    'port': 33060,
    'user': 'root',
    'password': '1732',
    'schema': 'projekt'
})


def closeSession():
	session.close()
	return 0


def storeCostumer(dataList):

	#Check if cosutmer already exists, i assume that a costumer only has 1 phonenumber
	custID = 0;

	query = "SELECT customerID, address,city,zipcode,phoneNr,eMail FROM Customer "+ \
	f"WHERE phoneNr = {dataList[5]}"
	try:
		result = session.sql(query).execute()
		data = result.fetch_all()

		if len(data) == 0:
			## Ny kund
			query = "INSERT INTO Customer (firstName,lastName,address,city,zipCode,phoneNr,eMail) VALUES "+ \
			f"('{dataList[0]}','{dataList[1]}','{dataList[2]}','{dataList[3]}','{dataList[4]}','{dataList[5]}','{dataList[6]}');"
			session.sql(query).execute()

			#Get the new id!
			query = f"SELECT LAST_INSERT_ID();"
			result = session.sql(query).execute()
			custID = result.fetch_all()[0][0]
		else: 

			query = "UPDATE Customer " + \
			f"SET firstName = '{dataList[0]}', lastName = '{dataList[1]}', address = '{dataList[2]}', city = '{dataList[3]}', zipCode = '{dataList[4]}', eMail = '{dataList[6]}' "+ \
			f"WHERE customerID = '{data[0][0]}';"
			print(query)
			session.sql(query).execute()
			custID = data[0][0]
	except DatabaseError as error:
		print("ERROR : Database error noticed: ",error)

	return custID


def getBook(coursenumber):
	'''Function returns given course literature data'''
	query = f"SELECT b.bookName, b.author, b.price, b.ISBN, c.courseName"+ \
	f" FROM book b INNER JOIN course c ON {coursenumber} = c.courseID AND {coursenumber} = b.courseID;"
	data = []

	try:
		result = session.sql(query).execute()
		data = result.fetch_all()[0]
	except DatabaseError as error:
		print("ERROR : Database error noticed: ",error)

	return data


def getBookCost(quantity,bookID):
	'''Uses the function in sql. Returns cost for x amount of books'''
	query = f"SELECT countBookCost({quantity},{bookID});"
	bookCost = []

	try:
		result = session.sql(query).execute()
		bookCost = result.fetch_all()[0]
	except DatabaseError as error:
		print("ERROR : Database error noticed: ",error)

	return bookCost


def getCartData(sessionDict):
	'''Returns cart invoice and dict with booknames'''
	invoice = 0
	cleanDict = {}
	try:
		for key,value in sessionDict.items():
			if key != '_permanent':
				invoice += getBookCost(value,key)[0]

				query = f"SELECT bookName FROM Book WHERE {key} = bookID"
				result = session.sql(query).execute()
				data = result.fetch_all()[0]
				cleanDict[data[0]] = value
	except DatabaseError as error:
		print("ERROR : Database error noticed: ",error)

	return cleanDict,invoice


def storeOrder(sessionDict,customerID):
	'''Stores the order for staff, Returns ordernumber for the costumer'''
	orderID = None
	try:
		_,invoice = getCartData(sessionDict)
		## Store the new order
		query = "INSERT INTO Orders (customerID,invoice,dateofOrder) VALUES "+ \
		f"('{customerID}','{invoice}',CURDATE());";
		session.sql(query).execute()
		# Get orderID to return it
		query = f"SELECT LAST_INSERT_ID();"
		result = session.sql(query).execute()
		orderID = result.fetch_all()[0][0]
		storeOrderDetails(sessionDict,orderID)
	except DatabaseError as error:
		print("ERROR : Database error noticed: ",error)

	return orderID


def storeOrderDetails(sessionDict,orderID):
	try:
		for key,value in sessionDict.items():
			if key != '_permanent':
				query = "INSERT INTO Orderdetails (bookID,orderID,quantity) VALUES "+ \
				f"('{key}','{orderID}','{value}');";
				session.sql(query).execute()
	except DatabaseError as error:
		print("ERROR : Database error noticed: ",error)


def getTopList():
	query = "SELECT b.bookName,b.author,s.salescount FROM Book b "+ \
	"INNER JOIN bestseller s ON s.bookID = b.bookID " + \
	"ORDER BY s.salescount DESC " + \
	"limit 3;"

	data = []

	try:
		result = session.sql(query).execute()
		data = result.fetch_all()
	except DatabaseError as error:
		print("ERROR : Database error noticed: ",error)

	return data

def getDonatedMoney():
	donated = None
	try:
		query = "SELECT countDonatedMoney();"
		result = session.sql(query).execute()
		donated = result.fetch_all()
		if donated[0][0] == None:
			donated = 0
		else:
			donated = donated[0][0]
	except DatabaseError as error:
		print("ERROR : Database error noticed: ",error)

	return donated


