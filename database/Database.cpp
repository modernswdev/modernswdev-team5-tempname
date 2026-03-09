#include "Database.h"
#include <iostream>

Database::Database() {
    db = nullptr;
    connected = false;
}

Database::~Database() {
    if (db != nullptr) {
        sqlite3_close(db);
    }
}

bool Database::open(const std::string& dbName) {

    int check = sqlite3_open(dbName.c_str(), &db);

    if (check == SQLITE_OK) {
        connected = true;
        std::cout << "Connected to database." << std::endl;
        return true;
    } else {
        std::cout << "Error connecting to database." << std::endl;
        return false;
    }
}

void Database::close() {

    if (db != nullptr) {
        sqlite3_close(db);
        connected = false;
        std::cout << "Database closed." << std::endl;
    }

}

bool Database::isOpen() const {
    return connected;
}