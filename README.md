# SQL Assist
The SQL Assist system backend is a code assistance system that allows users to visualise SQL commands for those with negligible coding experience.

## Connecting to the API
The API can be connected with the following connection string:
```
http://ec2-18-234-188-126.compute-1.amazonaws.com/
```
Followed by the endpoint
- testconnect/ : Tests your connection to the SQL server
- getmetadata/ : Gets the metadata for the database
- listdbs/ : List the databases on the server
- listtables/ : List all tables in the selected database
- listcolumns/ : List all columns in the selected database

## Request String
Make a POST request with a JSON string as described below:
```
{
	"server": "database-1.cyw17x3tauzw.us-east-1.rds.amazonaws.com",
	"user": "admin",
	"password": "password",
	"dbtype": "sqlserver",
	"dbname": "testdb",
	"tablename": "Persons"
}
```
The API has the following parameters

- server : currently set to AWS RDS connection link
- user/password : user/password of the SQL server
- dbname/dbtype : database name and type
- tablename : (optional) name of table for which you need columns