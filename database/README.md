# Database

This project uses SQLite for the service request database.

To create the database locally run:

sqlite3 database/service_requests.db < database/schema.sql

This will create the local database file for development. 

This allows the application to open and close a database connection which will be used later for managing service requests.