CREATE DATABASE HospitalMS;

USE HospitalMS;

-- DROP DATABASE hospitalms;

-- strong 
CREATE TABLE Hospital(Branch_ID INT PRIMARY KEY,
					  H_Name VARCHAR(50) NOT NULL,
                      Address VARCHAR(255));

-- strong
CREATE TABLE Employee(Emp_ID INT PRIMARY KEY AUTO_INCREMENT,
					  Emp_Name VARCHAR(50) NOT NULL,
                      Salary INT CHECK(Salary>0),
                      DOJ DATE NOT NULL,					
                      MGR_ID INT,
                      FOREIGN KEY(MGR_ID) REFERENCES Employee(Emp_ID),
                      Branch_ID INT NOT NULL,
                      FOREIGN KEY(Branch_ID) REFERENCES Hospital(Branch_ID));
               
-- strong
CREATE TABLE Doctor(Emp_ID INT,
					FOREIGN KEY(Emp_ID) REFERENCES Employee(Emp_ID),
                    Qualification VARCHAR(50) NOT NULL,
                    PRIMARY KEY(Emp_ID));

-- strong
CREATE TABLE Nurse(Emp_ID INT,
				   FOREIGN KEY(Emp_ID) REFERENCES Employee(Emp_ID),
                   Roles VARCHAR(50),
                   PRIMARY KEY(Emp_ID));
        
-- weak
CREATE TABLE Room(Room_no INT,
				  Branch_ID INT NOT NULL,
				  FOREIGN KEY(Branch_ID) REFERENCES Hospital(Branch_ID),	
				  R_Type VARCHAR(25),
                  Capacity INT CHECK(Capacity > 0),
                  Available INT,
                  PRIMARY KEY(Branch_ID, Room_no));
                  
DELIMITER //

CREATE TRIGGER BeforeRoomInsert
BEFORE INSERT ON Room
FOR EACH ROW
BEGIN
    -- Check if the new room's availability is greater to its capacity
    IF NEW.Available > NEW.Capacity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Room availability cannot exceed room capacity';
    END IF;
END //

DELIMITER ;

DELIMITER //
CREATE TRIGGER SetNull
BEFORE INSERT ON Patient
FOR EACH ROW
BEGIN
	SET NEW.P_Name = NULLIF(NEW.P_Name, '');
END //
DELIMITER ;
          
-- strong
CREATE TABLE Patient(PID INT PRIMARY KEY auto_increment,
					 P_Name VARCHAR(50) NOT NULL,
                     DOB DATE,
                     Sex CHAR,
                     Address VARCHAR(255),
                     Branch_ID INT NOT NULL,
                     Room_no INT NOT NULL,
					 FOREIGN KEY(Branch_ID, Room_no) REFERENCES Room(Branch_ID, Room_no));
                      
              
-- strong
CREATE TABLE Patient_Records(Record_no INT PRIMARY KEY AUTO_INCREMENT,
							 PID INT NOT NULL,
                             FOREIGN KEY(PID)REFERENCES Patient(PID),
                             Treatment_Type VARCHAR(50),
                             Date DATE,
                             Bill INT CHECK(Bill>0));
                      
-- associative
CREATE TABLE Treatment(Emp_ID INT,
					   FOREIGN KEY(Emp_ID) REFERENCES Doctor(Emp_ID),
                       PID INT,
					   FOREIGN KEY(PID) REFERENCES Patient(PID),
                       Date_Start DATE NOT NULL,
                       Date_end DATE,
                       PRIMARY KEY(Emp_ID, PID));
            
-- associative
CREATE TABLE Cares_for(Emp_ID INT,
					   FOREIGN KEY(Emp_ID) REFERENCES Nurse(Emp_ID),
                       PID INT,
					   FOREIGN KEY(PID) REFERENCES Patient(PID),
                       Shift VARCHAR(10),
                       PRIMARY KEY(Emp_ID, PID));
                       
-- PROCEDURE
DELIMITER //
CREATE PROCEDURE GetRoomAvailability(IN BranchID INT, IN RoomNo INT, OUT RoomAvailability INT, OUT ErrorMessage VARCHAR(50))
BEGIN
    DECLARE V_Branch INT DEFAULT 0;
    DECLARE V_Room INT DEFAULT 0;
    
    
    DECLARE EXIT HANDLER FOR NOT FOUND
        BEGIN
            IF V_Branch = 0 THEN
				SET ErrorMessage = 'Branch not found';
            ELSEIF V_Room = 0 THEN
				SET ErrorMessage = 'Room not found in the specified branch';
            END IF;
        END;

    -- Check if the branch exists
    SELECT Branch_ID INTO V_Branch
    FROM Hospital
    WHERE Branch_ID = BranchID;

    -- Check if the room exists in the specified branch
    SELECT Room_no INTO V_Room
    FROM Room
    WHERE Branch_ID = BranchID AND Room_no = RoomNo;

    -- Retrieve the availability of the room
    SELECT Available INTO RoomAvailability
    FROM Room
    WHERE Branch_ID = BranchID AND Room_no = RoomNo;

END//
DELIMITER ;

-- TRIGGER
DELIMITER //
CREATE TRIGGER Patient_AfterInsert
AFTER INSERT ON Patient
FOR EACH ROW
BEGIN
    DECLARE RoomAvail INT;
    DECLARE ErrorMessage VARCHAR(50);
    
    -- Call the GetRoomAvailability Procedure to get room availability
    CALL GetRoomAvailability(NEW.Branch_ID, NEW.Room_no, RoomAvail, ErrorMessage);
    
    IF 	ErrorMessage IS NOT NULL THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = ErrorMessage;
	ELSEIF RoomAvail > 0 THEN
		-- Decrement the room availability by 1
        UPDATE Room
        SET Available = Available - 1
        WHERE Branch_ID = NEW.Branch_ID AND Room_no = NEW.Room_no;
    ELSEIF RoomAvail <= 0 THEN
		-- Room not available
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Room is not available.';
    END IF;
    
END//
DELIMITER ;

insert into Hospital values(1, 'aryabhatta', 'kothrud');
insert into Hospital values(2, 'kashyap', 'kothrud');
insert into Hospital values(3, 'ganaga', 'kothrud');

select * from Hospital; 

Insert into room values(11, 1, 'ac', 100, 100);
Insert into room values(12, 2, 'ac', 10, 10);
Insert into room values(13, 2, 'ac', 10, 0);
Insert into room values(13, 3, 'ac', -1, 10); -- error code 3819 "check constraint voilated"
Insert into room values(13, 2, 'ac', 10, 20); -- error code 1644 "in room availability > capacity"


select * from room;

insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 2, 12);
insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 2, 13); -- error code 1644 "room avialibility <= 0"
insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 1, 11);
insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 3, 12);-- error code 1452 "referenced foreign key(branch id) not found"
insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 1, 12);-- error code 1452 "referenced foreign key(room no) not found"



insert into Employee values (10, NULL, 122, '12-12-12', 10, 1);-- error code 1048 for not null

DELETE FROM Patient WHERE PID = 1;
DELETE FROM Patient WHERE PID = 2;
DELETE FROM Patient WHERE PID = 3;
DELETE FROM Patient WHERE PID = 4;
DELETE FROM Patient WHERE PID = 5;
DELETE FROM Patient WHERE PID = 6;
DELETE FROM Patient WHERE PID = 7;
DELETE FROM Patient WHERE PID = 8;
DELETE FROM Patient WHERE PID = 9;

select * from patient;
ALTER TABLE PATIENT AUTO_INCREMENT=1;










                       
