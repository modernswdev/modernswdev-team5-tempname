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

    bool emailExists(const std::string& email);
    bool createUser(const std::string& firstName, const std::string& lastName, const std::string& email, const std::string& password);

};

#endif 
