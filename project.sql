use restaurant_reservation;

alter table users
modify First_Name VARCHAR(255) NOT NULL,
modify Last_Name VARCHAR(255) NOT NULL,
modify Phone_Number VARCHAR(255) NOT NULL,
modify Email VARCHAR(255) NOT NULL,
modify Password VARCHAR(255) NOT NULL;

alter table users
add primary key (email);

delete from users
order by first_name desc limit 1;

CREATE TABLE Bookings (
Table_Name VARCHAR(255),
Capacity VARCHAR(255),
Name VARCHAR(255), 
Phone VARCHAR(255),
Email VARCHAR(255),
Date VARCHAR(255),
Time VARCHAR(255),
Booked BOOL
);

INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 1", "2");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 2", "2");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 3", "2");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 4", "2");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 5", "2");

INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 6", "4");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 7", "4");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 8", "4");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 9", "4");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 10", "4");

INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 11", "6");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 12", "6");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 13", "6");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 14", "6");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 15", "6");

INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 16", "8");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 17", "8");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 18", "8");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 19", "8");
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 20", "8");

ALTER TABLE Bookings
ADD PRIMARY KEY (Table_Name);

UPDATE Bookings
SET Booked = 0;

UPDATE Bookings
SET name=NULL,phone=NULL,email=NULL,date=NULL, time=NULL,Booked = 0;
delete from users;