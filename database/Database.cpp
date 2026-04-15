#include "Database.h"
#include <iostream>

Database::Database() {
    db = nullptr;
    connected = false;
}

Database::~Database() {
    close();
}


bool Database::open(const std::string& dbName) {
    if (db != nullptr) {
        close();
    }

    int check = sqlite3_open(dbName.c_str(), &db);

    if (check == SQLITE_OK) {
        connected = true;
        std::cout << "Connected to database." << std::endl;
        return true;
    } else {
        std::cout << "Error connecting to database." << std::endl;
        if (db != nullptr) {
            sqlite3_close(db);
            db = nullptr;
        }
        connected = false;
        return false;
    }
}

void Database::close() {

    if (db != nullptr) {
        sqlite3_close(db);
        db = nullptr
        connected = false;
        std::cout << "Database closed." << std::endl;
    }

}

bool Database::isOpen() const {
    return connected;
}

bool Database::emailExists(const std::string& email) {
    if (!connected || db == nullptr) {
        return false;
    }

    const char* sql = "SELECT 1 FROM Users WHERE UserEmail = ? LIMIT 1;";
    sqlite3_stmt* stmt = nullptr;

    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cout << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
        return false;
    }

    sqlite3_bind_text(stmt, 1, email.c_str(), -1, SQLITE_TRANSIENT);

    bool exists = (sqlite3_step(stmt) == SQLITE_ROW);

    sqlite3_finalize(stmt);
    return exists;
}

bool Database::createUser(const std::string& firstName, const std::string& lastName, const std::string& email, const std::string& password) {
    if (!connected || db == nullptr) {
        std::cout << "Database not connected." << std::endl;
        return false;
    }

    if (emailExists(email)) {
        std::cout << "Email already exists." << std::endl;
        return false;
    }

    const char* sql = "INSERT INTO Users (UserFirstName, UserLastName, UserEmail, UserPassword) VALUES (?, ?, ?, ?);";
    
    sqlite3_stmt* stmt = nullptr;

    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cout << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
        return false;
    } 

    sqlite3_bind_text(stmt, 1, firstName.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, lastName.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 3, email.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 4, password.c_str(), -1, SQLITE_TRANSIENT);

    rc = sqlite3_step(stmt);

    if (rc != SQLITE_DONE) {
        std::cout << "Failed to execute statement: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_finalize(stmt);
        return false;
    }

    sqlite3_finalize(stmt);
    std::cout << "User created successfully." << std::endl;
    return true;
}

