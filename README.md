This is a collection of scripts used in my WayStream Senior Capstone
--------------------------------------------------------------------

subToSystemTopic:       Bootup script executed by RPi to subscribe to AWS IoT Core topic to enable communication between RPi and Android Application

CreateDatabaseScript:   MySQL script for creation of database and command reference

system_io:              GPIO control to open a relay enabling a connected system to receive power

run_system:             Calls system_io and records duration of run time onto AWS RDS

Email_Confirmation_API: Lambda function of javascript that sends a confirmation email to new users

IoT_Core_API:           Lambda function of initial API for direct communication between application and RPi

RDS_API:                API structure for database calls using AWS Lambda