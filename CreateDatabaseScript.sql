/*
 Author: Jacob Chesley
 
 Version 1 WIP
 Last Update 2/28/19
 */

CREATE DATABASE WayStream_Prod;
USE WayStream_Prod;

CREATE TABLE User (
  First_Name VARCHAR(25), 
  Last_Name VARCHAR(25), 
  Email VARCHAR(40) NOT NULL, 
  Username VARCHAR(25) NOT NULL, 
  Secure_Password VARCHAR(64) NOT NULL,
  Salt_ID INT NOT NULL,
  Confirmed_Email BOOL DEFAULT FALSE,
  User_ID INT NOT NULL AUTO_INCREMENT UNIQUE,
  PRIMARY KEY (User_ID)
);

# System is a generic expandable (through Sys_Type) table that enables any type of IOT product to be added
# A System_Properties table will be added for each type of Sys_Type as needed 
CREATE TABLE System (
  Sys_Name VARCHAR(25),
  Sys_Type ENUM('Valve', 'Light', 'Circuit') CHARACTER SET BINARY NOT NULL,
  Sys_ID VARCHAR(36) NOT NULL UNIQUE,
  User_ID INT DEFAULT 0,
  Time_Linked TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (Sys_ID),
  FOREIGN KEY (User_ID) REFERENCES User (User_ID)
);

# System properties geared specifically towards the valve system
CREATE TABLE Valve_System_Properties (
  Prop_ID VARCHAR(36),
  Last_Connection TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Location FLOAT(2),
  Sys_ID VARCHAR(36),
  Flow_Rate FLOAT(1),
  Voltage FLOAT(1) DEFAULT 12,
  PRIMARY KEY (Prop_ID),
  FOREIGN KEY (Sys_ID) REFERENCES System (Sys_ID)
);

CREATE TABLE Statistics (
  Stat_ID VARCHAR(36),
  Prop_ID VARCHAR(36),
  Update_Times BLOB(1),
  Moisture_Pct BLOB(1),
  PRIMARY KEY (Stat_ID),
  FOREIGN KEY (Prop_ID) REFERENCES Valve_System_Properties (Prop_ID)
);
        
# TODO: Without constant indexing, if this were released,
# this would become bloated and unusable. I need to find
# a better way to store these runtimes.
#
# TODO: I should also check on a better way to delete times
# that have already passed.
CREATE TABLE Runtime_Event (
  Sys_ID VARCHAR(36),
  Runtime_ID VARCHAR(36) NOT NULL UNIQUE,
  Runtime_Name VARCHAR(36),
  Color VARCHAR(7),
  Start_Year INT,
  Start_Month INT,
  Start_Day INT,
  Start_Hour INT,
  Start_Minute INT,
  End_Year INT,
  End_Month INT,
  End_Day INT,
  End_Hour INT,
  End_Minute INT,
  PRIMARY KEY (Runtime_ID),
  FOREIGN KEY (Sys_ID) REFERENCES System (Sys_ID)
);

# For system to report IP upon booting.
# This is for development and not for release.
# Enables headless development.
CREATE TABLE Admin_IP (
  SaveTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  IP_Address VARCHAR(20),
  PRIMARY KEY (SaveTime)
);

# Records the times at which each system is on
CREATE TABLE System_Runtime (
  Entry_Value INT NOT NULL AUTO_INCREMENT,
  Sys_ID VARCHAR(36) NOT NULL,
  StartTime INT NULL,
  StopTime INT NULL,
  PRIMARY KEY (Entry_Value)
);

DELIMITER $$

DROP TRIGGER IF EXISTS Unix_Time$$

CREATE TRIGGER Unix_Time BEFORE INSERT ON System_Runtime FOR EACH ROW
BEGIN
  IF (NEW.StartTime IS NULL)
  THEN
    SET NEW.StartTime := UNIX_TIMESTAMP();
  END IF;
END $$

DROP FUNCTION IF EXISTS Update_StopTime$$

CREATE FUNCTION Update_StopTime (start_time INT, entry INT)
  RETURNS BOOL
    DETERMINISTIC
    BEGIN
      UPDATE System_Runtime SET StopTime = UNIX_TIMESTAMP() WHERE (StartTime = start_time) AND (Entry_Value = entry);
	  RETURN TRUE;
	END $$

DELIMITER ;

# Create Admin account for default system ownership
INSERT INTO User (First_Name, Last_Name, Email, Username, Secure_Password, Salt_ID, Confirmed_Email) VALUES("Admin", "Admin", "test@gmail.com", "rein", "admin", 1, 1);
INSERT INTO System (Sys_Name, Sys_Type, Sys_ID, User_ID) VALUES("Blue", "Valve", "783c7e66-13ac-42a7-bf0e-4eeed6423280", "1"); # Blue:1 system for testing
INSERT INTO System (Sys_Name, Sys_Type, Sys_ID, User_ID) VALUES("Green", 1, "e7e31cee-17fe-41c8-aa65-d8df9334178e", "1"); # Green:2 system for testing

SELECT * FROM WayStream_Prod.User;
SELECT * FROM WayStream_Prod.Admin_IP;
SELECT * FROM WayStream_Prod.System;
SELECT * FROM WayStream_Prod.System_Runtime;
SELECT * FROM WayStream_Prod.Runtime_Event WHERE Sys_ID = "783c7e66-13ac-42a7-bf0e-4eeed6423280";