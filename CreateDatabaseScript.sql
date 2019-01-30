/*
 Author: Jacob Chesley
 
 Rough draft
 Last Update 1/30/19
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
  Last_Connection TIMESTAMP(1) DEFAULT CURRENT_TIMESTAMP,
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

CREATE TABLE Runtime (
  Runtime_ID VARCHAR(36),
  Prop_ID VARCHAR(36),
  Day_ID ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') CHARACTER SET BINARY,
  Start_Time TIMESTAMP(1),
  Duration TIME(1),
  Repeat_Daily BOOL DEFAULT FALSE,
  Repeat_Monthly BOOL DEFAULT FALSE,
  Repeat_Yearly BOOL DEFAULT FALSE,
  PRIMARY KEY (Runtime_ID),
  FOREIGN KEY (Prop_ID) REFERENCES Valve_System_Properties (Prop_ID)
);

# Create Admin account for default system ownership
INSERT INTO User (First_Name, Last_Name, Email, Username, Secure_Password, Salt_ID) VALUES("Admin", "Admin", "tierein@gmail.com", "tierein", "admin", 1);
INSERT INTO System (Sys_ID, User_ID) VALUES("783c7e66-13ac-42a7-bf0e-4eeed6423280", "1");

# Testing calls
DELETE FROM User WHERE (User_ID = 2);
#DELETE FROM System WHERE (User_ID = 1);

SELECT * FROM WayStream_Prod.User;
SELECT * FROM WayStream_Prod.System;