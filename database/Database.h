#ifndef DATABASE_H
#define DATABASE_H

#include <string>
#include <sqlite3.h>

class Database {

private:
    sqlite3* db;
    bool connected;

public:
    Database();
    ~Database();

    bool open(const std::string& dbName);
    void close();
    bool isOpen() const;

};

#endif 
