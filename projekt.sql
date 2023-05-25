CREATE DATABASE IF NOT EXISTS projekt;
USE projekt;

CREATE TABLE Customer (
	customerID int NOT NULL AUTO_INCREMENT,
	firstName varchar (255) NOT NULL,
    lastName varchar (255) NOT NULL,
	address varchar(255) NOT NULL,
	city varchar(255) NOT NULL,
	zipCode varchar(255) NOT NULL, ###Because of blankspace i guess , could be int but varchar works
	phoneNr varchar(255) NOT NULL,
	eMail varchar(255) NOT NULL,

	PRIMARY KEY (customerID)
);

CREATE TABLE Course (
	courseID int NOT NULL AUTO_INCREMENT,
	courseName varchar(255),
	PRIMARY KEY (courseID)

);

CREATE TABLE Orders (
	orderID int NOT NULL AUTO_INCREMENT,
	customerID int, 
	invoice int NOT NULL,
	dateOfOrder date,

	PRIMARY KEY (orderID),
    FOREIGN KEY (customerID) REFERENCES Customer(customerID)

);

CREATE TABLE Book (
	bookID int NOT NULL AUTO_INCREMENT, 
	courseID int,
	bookName varchar(255) NOT NULL,
	author varchar(255) NOT NULL,
	price int NOT NULL,
	ISBN varchar(255) NOT NULL,

	PRIMARY KEY (bookID),
	FOREIGN KEY (courseID) REFERENCES Course(courseID)

);

CREATE TABLE OrderDetails (
	detailID int NOT NULL AUTO_INCREMENT,
	bookID int, 
	orderID int,
	quantity int NOT NULL,

	PRIMARY KEY (detailID),
	FOREIGN KEY (bookID) REFERENCES Book(bookID), 
	FOREIGN KEY (orderID) REFERENCES Orders(orderID)


);

CREATE TABLE bestSeller (
	topID int NOT NULL AUTO_INCREMENT,
	bookID int, 
	salescount int NOT NULL,

	PRIMARY KEY (topID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID)

);


DROP FUNCTION IF EXISTS countBookCost;
DELIMITER \\
CREATE FUNCTION countBookCost(quantity INT, bookID INT)
RETURNS INTEGER DETERMINISTIC
BEGIN 
	DECLARE bookCost INTEGER;
	DECLARE totalBookCost INTEGER;

	SELECT b.price INTO bookCost FROM Book b WHERE b.bookID = bookID;

	SET totalBookCost = (bookCost * quantity);
	RETURN (totalBookCost);
END \\
DELIMITER ;


DROP TRIGGER IF EXISTS update_bestseller;
DELIMITER \\ 
CREATE TRIGGER update_bestseller
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN 
	DECLARE sales INTEGER;
	SET sales = NEW.quantity;

	UPDATE bestSeller SET salescount = (salescount + sales) WHERE bookID = NEW.bookID;

END \\ 
DELIMITER ;


DROP FUNCTION IF EXISTS countDonatedMoney;
DELIMITER \\
CREATE FUNCTION countDonatedMoney()
RETURNS INTEGER DETERMINISTIC
BEGIN 
	DECLARE totalSales INTEGER;
	DECLARE amountDonated INTEGER;

	SELECT SUM(invoice) INTO totalSales FROM Orders;

	SET amountDonated = (totalSales * 0.1);
	RETURN (amountDonated);
END \\
DELIMITER ;