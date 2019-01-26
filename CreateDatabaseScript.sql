/*
 Author: Jacob Chesley
 
 Initial rough draft
 Last Update 1/25/19
 */

CREATE DATABASE WayStream_Prod;
USE WayStream_Prod;

CREATE TABLE User (
  First_Name VARCHAR(25), 
  Last_Name VARCHAR(25), 
  Email VARCHAR(40), 
  Username VARCHAR(25), 
  Secure_Password VARCHAR(200), 
  User_ID VARCHAR(36), 
  PRIMARY KEY (User_ID)
);

CREATE TABLE System (
  Sys_Name VARCHAR(25),
  Sys_Type VARCHAR(25),
  Sys_ID VARCHAR(36),
  User_ID VARCHAR(36),
  Time_Linked TIMESTAMP(1),
  PRIMARY KEY (Sys_ID),
  FOREIGN KEY (User_ID) REFERENCES User (User_ID)
);

CREATE TABLE System_Properties (
  Prop_ID VARCHAR(36),
  Last_Connection TIMESTAMP(1),
  Location FLOAT(2),
  Sys_ID VARCHAR(36),
  Flow_Rate FLOAT(1),
  PRIMARY KEY (Prop_ID),
  FOREIGN KEY (Sys_ID) REFERENCES System (Sys_ID)
);

CREATE TABLE Statistics (
  Stat_ID VARCHAR(36),
  Prop_ID VARCHAR(36),
  Update_Times BLOB(1),
  Moisture_Pct BLOB(1),
  PRIMARY KEY (Stat_ID),
  FOREIGN KEY (Prop_ID) REFERENCES System_Properties (Prop_ID)
);

CREATE TABLE Runtime (
  Runtime_ID VARCHAR(36),
  Prop_ID VARCHAR(36),
  Day_ID ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') CHARACTER SET BINARY,
  Start_Time TIMESTAMP(1),
  Duration TIME(1),
  Repeat_Daily BOOL,
  Repeat_Monthly BOOL,
  Repeat_Yearly BOOL,
  PRIMARY KEY (Runtime_ID),
  FOREIGN KEY (Prop_ID) REFERENCES System_Properties (Prop_ID)
);

INSERT INTO User (First_Name, Last_Name, Email, Username, Secure_Password, User_ID) VALUES("Jacob", "Chesley", "tierein@gmail.com", "tierein", "123", "1234567890");

DELETE FROM User WHERE (User_ID = "1234567890");

SELECT * FROM WayStream_Prod.User;