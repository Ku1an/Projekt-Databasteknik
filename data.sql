INSERT INTO Course (courseName) VALUES
('Databasteknik'),
('Datorteknik'),
('Endimensionell analys'),
('Programmering i python'),
('Industriell ekonomi');

INSERT INTO Book (courseID,bookName,author,price,ISBN) VALUES 
(1,'Databasteknik','Thomas Padron-McCarthy och Tore Risch',579,'978-91-44-06919-7'),
(4,'A Beginners Guide to Python 3 Programming','John Hunt',489,'978-3-030-20289-7'),
(3,'Endimensionell analys','Jonas Månsson och Patrick Nordbeck', 499,'978-91-44-05610-4'),
(5,'Industrial Management','Mats Engwall, Anna Jerbrandt',349, '978-91-44-10788-2'),
(2,'Computer Organization and Design ARM Edition','David Patterson John Hennesy',999,'978-0-12-801733-3');

INSERT INTO bestSeller (bookID,salesCount) VALUES
(1,0),
(2,0),
(3,0),
(4,0),
(5,0);
