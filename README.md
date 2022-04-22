# SQL Assist
The SQL Assist system backend is a code assistance system that allows users to visualise SQL commands for those with negligible coding experience.


## JSON Response String
```
{
	"server": "database-1.cyw17x3tauzw.us-east-1.rds.amazonaws.com",
	"user": "admin",
	"password": "password",
	"dbname": "testdb",
	"dbtype": "sqlserver",
	"tablename": "Persons"
}
```
The API has the following parameters

- server : currently set to AWS RDS connection link
- user/password : user/password of the SQL server
- dbname/dbtype : database name and type
- tablename : (optional) name of table for which you need columns

