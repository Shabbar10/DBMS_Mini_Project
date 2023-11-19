CREATE DATABASE HospitalMS;

USE HospitalMS;

DROP DATABASE hospitalms;

-- Hospital Table(Strong)
CREATE TABLE Hospital(Branch_ID INT PRIMARY KEY,
					  Branch_Name VARCHAR(50) NOT NULL,
                      Address VARCHAR(255));
                
-- trigger for branch_name not null constraint
DELIMITER //
CREATE TRIGGER SetNullBranch_Name
BEFORE INSERT ON Hospital
FOR EACH ROW
BEGIN
	-- check if Branch name is not null
	SET NEW.Branch_Name = NULLIF(NEW.Branch_Name, '');
END //
DELIMITER ;

-- Employee Table (strong)
CREATE TABLE Employee(Emp_ID INT PRIMARY KEY AUTO_INCREMENT,
					  Emp_Name VARCHAR(50) NOT NULL,
                      Salary INT CHECK(Salary>0),
                      DOJ DATE,					
                      MGR_ID INT,
						FOREIGN KEY(MGR_ID) REFERENCES Employee(Emp_ID) ON DELETE SET NULL,
                      Branch_ID INT NOT NULL,
						FOREIGN KEY(Branch_ID) REFERENCES Hospital(Branch_ID) ON DELETE CASCADE);
                      
ALTER TABLE Employee AUTO_INCREMENT = 1111;

-- trigger for Emp_name not null constraint
DELIMITER //
CREATE TRIGGER SetNullEmp_Name
BEFORE INSERT ON Employee
FOR EACH ROW
BEGIN
	-- check if Employee name is not null
	SET NEW.Emp_Name = NULLIF(NEW.Emp_Name, '');
END //
DELIMITER ;

DROP TABLE Employee;

DELIMITER //
CREATE TRIGGER SetNullMGR_ID
BEFORE UPDATE ON Employee
FOR EACH ROW
BEGIN
	-- check if Employee name is not null
	SET NEW.MGR_ID = NULLIF(NEW.MGR_ID, 'None');
END //
DELIMITER ;

-- trigger for Branch_ID not null constraint
DELIMITER //
CREATE TRIGGER SetNullBranch_ID
BEFORE INSERT ON Employee
FOR EACH ROW
BEGIN
	-- check if Branch_ID is not null
	SET NEW.Branch_ID = NULLIF(NEW.Branch_ID, '');
END //
DELIMITER ;
               
-- Doctor Table (strong)
CREATE TABLE Doctor(Emp_ID INT,
					FOREIGN KEY(Emp_ID) REFERENCES Employee(Emp_ID) ON DELETE CASCADE,
                    Qualification VARCHAR(50) NOT NULL,
                    PRIMARY KEY(Emp_ID));
                    
-- trigger for Qualification not null constraint
DELIMITER //
CREATE TRIGGER SetNullQualification
BEFORE INSERT ON Doctor
FOR EACH ROW
BEGIN
	-- check if Qualification is not null
	SET NEW.Qualification = NULLIF(NEW.Qualification, '');
END //
DELIMITER ;

-- Nurse Table (strong)
CREATE TABLE Nurse(Emp_ID INT,
				   FOREIGN KEY(Emp_ID) REFERENCES Employee(Emp_ID) ON DELETE CASCADE,
                   Roles VARCHAR(50),
                   PRIMARY KEY(Emp_ID));
                
-- trigger to check if emp_id alr exists in nurse table
DELIMITER //
CREATE TRIGGER Check_Doctor_ID
BEFORE INSERT ON Doctor
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT Emp_ID FROM Nurse WHERE Emp_ID = NEW.Emp_ID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Employee ID already exists in Nurse table';
    END IF;
END//
DELIMITER ;

-- trigger to check if emp_id alr exists in doctor table
DELIMITER //
CREATE TRIGGER Check_Nurse_ID
BEFORE INSERT ON Nurse
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT Emp_ID FROM Doctor WHERE Emp_ID = NEW.Emp_ID) THEN
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'Employee ID already exists in Doctor table';
    END IF;
END//
DELIMITER ;
        
-- Room Table (weak)
CREATE TABLE Room(Room_no INT,
				  Branch_ID INT,
				  FOREIGN KEY(Branch_ID) REFERENCES Hospital(Branch_ID) ON DELETE CASCADE,	
				  R_Type VARCHAR(25),
                  Capacity INT CHECK(Capacity > 0),
                  Available INT,
                  PRIMARY KEY(Branch_ID, Room_no));
           
-- trigger for room availability < capacity constraint
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


          
-- Patient Table (strong)
CREATE TABLE Patient(PID INT PRIMARY KEY auto_increment,
					 P_Name VARCHAR(50) NOT NULL,
                     DOB DATE,
                     Sex CHAR,
                     Address VARCHAR(255),
                     Branch_ID INT NOT NULL,
                     Room_no INT NOT NULL,
					 FOREIGN KEY(Branch_ID, Room_no) REFERENCES Room(Branch_ID, Room_no) ON DELETE CASCADE);
					

-- -- trigger for P_name not null constraint
DELIMITER //
CREATE TRIGGER SetNullP_Name
BEFORE INSERT ON Patient
FOR EACH ROW
BEGIN
	-- check if patient name is not null
	SET NEW.P_Name = NULLIF(NEW.P_Name, '');
END //
DELIMITER ;

-- trigger for Branch_ID not null constraint
DELIMITER //
CREATE TRIGGER SetNullBranch_ID_P
BEFORE INSERT ON Patient
FOR EACH ROW
BEGIN
	-- check if Branch_ID is not null
	SET NEW.Branch_ID = NULLIF(NEW.Branch_ID, '');
END //
DELIMITER ;
              
-- trigger for Room_no not null constraint
DELIMITER //
CREATE TRIGGER SetNullRoom_no
BEFORE INSERT ON Patient
FOR EACH ROW
BEGIN
	-- check if Room_no is not null
	SET NEW.Room_no = NULLIF(NEW.Room_no, '');
END //
DELIMITER ;
              
-- Patient_Records Table (strong)
CREATE TABLE Patient_Records(Record_no INT PRIMARY KEY AUTO_INCREMENT,
							 PID INT NOT NULL,
                             FOREIGN KEY(PID)REFERENCES Patient(PID) ON DELETE NO ACTION,
                             Treatment_Type VARCHAR(50),
                             Date DATE,
                             Bill INT CHECK(Bill>0));
                      
ALTER TABLE Patient_Records AUTO_INCREMENT = 1001;

-- trigger for PID not null constraint
DELIMITER //
CREATE TRIGGER SetNullPID
BEFORE INSERT ON Patient_Records
FOR EACH ROW
BEGIN
	-- check if PID is not null
	SET NEW.PID = NULLIF(NEW.PID, '');
END //
DELIMITER ;
              
-- associative
CREATE TABLE Treatment(Emp_Id INT,
					   FOREIGN KEY(Emp_ID) REFERENCES Doctor(Emp_ID) ON DELETE CASCADE,
                       PID INT,
					   FOREIGN KEY(PID) REFERENCES Patient(PID) ON DELETE CASCADE,
                       Date_Start DATE,
                       Date_end DATE,
                       PRIMARY KEY(Emp_ID, PID));
                                   
-- associative
CREATE TABLE Cares_for(Emp_ID INT,
					   FOREIGN KEY(Emp_ID) REFERENCES Nurse(Emp_ID) ON DELETE CASCADE,
                       PID INT,
					   FOREIGN KEY(PID) REFERENCES Patient(PID) ON DELETE CASCADE,
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

-- ==========================================================DATA INPUT======================================================================================
-- HOSPITAL 
INSERT INTO Hospital VALUES(1182, 'CALIFORNIA SMASH',  'Kiyashi Ward');
INSERT INTO Hospital VALUES(1265, 'TEXAS SMASH',  'Hosu City');
INSERT INTO Hospital VALUES(1508, 'DETROIT SMASH',  'Nabu Island');
INSERT INTO Hospital VALUES(1468, 'NEBRASKA SMASH',  'Musutafu');

SELECT * FROM Hospital;

-- ROOMS
desc room;
INSERT INTO Room VALUES(101, 1265, 'AC', 5, 5);
INSERT INTO Room VALUES(201, 1182, 'AC', 10, 10);
INSERT INTO Room VALUES(102, 1508, 'Deluxe', 15, 15);
INSERT INTO Room VALUES(103, 1468, 'General', 25, 25);
INSERT INTO Room VALUES(301, 1265, 'Suite', 5, 5);
INSERT INTO Room VALUES(302, 1182, 'Isolation',25, 25);
INSERT INTO Room VALUES(204, 1508, 'AC-Deluxe', 12, 12);
INSERT INTO Room VALUES(301, 1468, 'General', 20, 20);
INSERT INTO Room VALUES(203, 1265, 'Isolation', 15, 15);
INSERT INTO Room VALUES(401, 1508, 'Deluxe', 10, 10);
INSERT INTO Room VALUES(404, 1468, 'AC-Deluxe', 7, 7);

SELECT * FROM Room;

desc Employee;

INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Shoto', 1000000, '2000-10-12', NULL, 1182);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Eijiro', 1000000, '2001-11-12', NULL, 1265);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Tenya', 1000000, '1999-06-11', NULL, 1508);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Mina', 1000000, '2000-07-01', NULL, 1468);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Shota', 100000, '2003-11-01', NULL, 1182);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Denki', 100000, '2004-03-20', NULL, 1265);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Dabi', 100000, '2005-10-10', NULL, 1508);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Endeavor', 100000, '2004-05-12', NULL, 1468);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Minoru', 10000, '2006-02-02', NULL, 1182);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Kurogiri', 10000, '2007-09-19', NULL, 1265);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Tomura', 10000, '2006-06-06', NULL, 1508);
INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Kyoka', 10000, '2008-02-03', NULL, 1468);

SELECT * FROM Employee;

UPDATE Employee SET MGR_ID = 1111 WHERE Emp_ID = 1115;
UPDATE Employee SET MGR_ID = 1112 WHERE Emp_ID = 1116;
UPDATE Employee SET MGR_ID = 1113 WHERE Emp_ID = 1117;
UPDATE Employee SET MGR_ID = 1114 WHERE Emp_ID = 1118;
UPDATE Employee SET MGR_ID = 1115 WHERE Emp_ID = 1119;
UPDATE Employee SET MGR_ID = 1116 WHERE Emp_ID = 1120;
UPDATE Employee SET MGR_ID = 1117 WHERE Emp_ID = 1121;
UPDATE Employee SET MGR_ID = 1118 WHERE Emp_ID = 1122;

INSERT INTO Doctor VALUES(1111, 'MS');
INSERT INTO Doctor VALUES(1112, 'DDM');
INSERT INTO Doctor VALUES(1113, 'MD');
INSERT INTO Doctor VALUES(1114, 'BUMS');
INSERT INTO Doctor VALUES(1115, 'MBBS');
INSERT INTO Doctor VALUES(1116, 'BSN');
INSERT INTO Doctor VALUES(1117, 'BHMS');
INSERT INTO Doctor VALUES(1118, 'BAMS');

SELECT  * FROM Doctor;

INSERT INTO Nurse VALUES(1119, 'Medical-Surgical');
INSERT INTO Nurse VALUES(1120, 'Anesthetist');
INSERT INTO Nurse VALUES(1121, 'Clinical');
INSERT INTO Nurse VALUES(1122, 'Occupational');

SELECT  * FROM Nurse;








-- =============================================================TEST CASES===========================================================================================
-- insert into Hospital values(1, 'aryabhatta', 'kothrud');
-- insert into Hospital values(2, 'kashyap', 'kothrud');
-- insert into Hospital values(3, 'ganaga', 'kothrud');


-- INSERT INTO Nurse VALUES(1118, 'Occupational'); -- error code 1644 (if emp_id alr exixts in doctor table)
-- INSERT INTO Doctor VALUES(1119, 'BAMS'); -- error code 1644 (if emp_id alr exixts in nurse table)

-- INSERT INTO Employee(Emp_Name, Salary, DOJ, MGR_ID, Branch_ID) VALUES('Kyoka', 10000, '2008-02-03', NULL, 1468);
-- INSERT INTO Doctor VALUES(1123, ''); error code 1048 (not null)


-- select * from Hospital; 

-- Insert into room values(11, 1, 'ac', 100, 100);
-- Insert into room values(12, 2, 'ac', 10, 10);
-- Insert into room values(13, 2, 'ac', 10, 0);
-- Insert into room values(13, 3, 'ac', -1, 10); -- error code 3819 "check constraint voilated"
-- Insert into room values(13, 2, 'ac', 10, 20); -- error code 1644 "in room availability > capacity"


-- select * from room;

-- insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 2, 12);
-- insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 2, 13); -- error code 1644 "room avialibility <= 0"
-- insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 1, 11);
-- insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 3, 12);-- error code 1452 "referenced foreign key(branch id) not found"
-- insert into patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values('surab', '1986-12-12', 'n', 'viman', 1, 12);-- error code 1452 "referenced foreign key(room no) not found"



-- insert into Employee values (10, NULL, 122, '12-12-12', 10, 1);-- error code 1048 for not null

-- DELETE FROM Patient WHERE PID = 1;
-- DELETE FROM Patient WHERE PID = 2;
-- DELETE FROM Patient WHERE PID = 3;
-- DELETE FROM Patient WHERE PID = 4;
-- DELETE FROM Patient WHERE PID = 5;
-- DELETE FROM Patient WHERE PID = 6;
-- DELETE FROM Patient WHERE PID = 7;
-- DELETE FROM Patient WHERE PID = 8;
-- DELETE FROM Patient WHERE PID = 9;

-- select * from patient;
-- ALTER TABLE PATIENT AUTO_INCREMENT=1;










                       
