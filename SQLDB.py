"""
File: SQLDB.py
Version: 1.0
Author: Surender Kumar
Copyright @ *****
Contact: emailsurenderkumar@gmail.com

This script will create the required tables into the MySQL database.
"""

# coding: utf-8
import sys
import MySQLdb
from EncDec import Security
import Logger

HOST_NAME = "localhost"
USER_NAME = "root"
DATABASE_NAME = "SKFlickrDB"

class MySQLDBSingleton (object):
    def __init__(self):
        self.id = self.__hash__()
        # Lets initialize a logger
        self.logH = Logger.getLogger()
        # Lets encrypt and save the MYSQL DB password.
        self.secObj = Security()
        self.secObj.genCipherPasswd() # Need to call only once
        self.hostName = HOST_NAME
        self.userName = USER_NAME
        self.dbName = DATABASE_NAME
        self.dbConnObj = MySQLdb.connect(self.hostName, self.userName,
                self.secObj.decPasswd())
        self.dbCursor = self.dbConnObj.cursor()

    @property
    def connection (self):
        return self.dbConnObj

    @property
    def cursor (self):
        return self.dbCursor

    def getHostName (self):
        return self.hostName

    def getUsrName (self):
        return self.userName

    def getSQLDBName (self):
        return self.dbName

    def exitDB (self):
        try:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        except:
            self.logH.error("Error commiting/closing DB.")
            exit()

    def createDB (self):
        crDBCmd = 'CREATE DATABASE '
        crDBCmd += self.dbName
        crDBCmd += ';'

        try:
            self.cursor.execute(crDBCmd)
            self.logH.debug("Creating DB: '" + self.dbName + "'")
        except:
            self.logH.error("Error creating DB: '" + self.dbName +
                    "', clean if already exist.")
            exit()

    def createTables (self):
        try:
            self.cursor.execute('USE ' + self.dbName + ';')
            # Creating 'user' table to store users' information.
            self.cursor.execute ("""
                   CREATE TABLE user
                   (
                     userid  VARCHAR(100),
                     username VARCHAR(100)
                   )ENGINE=INNODB;
                   """)
            self.logH.debug("Table 'user' created successfully.")

            # Creating 'links' table to store the connection information among users.
            self.cursor.execute ("""
                   CREATE TABLE links
                   (
                     userid1 VARCHAR(200),
                     userid2 VARCHAR(200)
                   )ENGINE=INNODB;
                   """)
            self.logH.debug("Table 'links' created successfully.")

            # Creating 'photo' table to store the photograph information of users.
            self.cursor.execute ("""
                   CREATE TABLE photo
                   (
                     photoid VARCHAR(200),
                     owner VARCHAR(200),
                     title VARCHAR(200)
                   )ENGINE=INNODB;
                   """)
            self.logH.debug("Table 'photo' created successfully.")

            # Creating 'tags' table to store the tags information of photographs.
            self.cursor.execute ("""
                   CREATE TABLE tags
                   (
                     tagid VARCHAR(200),
                     photoid VARCHAR(200),
                     tag VARCHAR(200)
                   )ENGINE=INNODB;
                   """)
            self.logH.debug("Table 'tags' created successfully.")
            self.logH.info("Tables have been created successfully.");
        except:
            self.logH.error("Failed to create tables for DB: '" + self.dbName + \
                    "' database.")
            exit()

"""
Creating a singleton DB instance, multi-threads may create problem otherwise
"""
instMySQLDB = MySQLDBSingleton()

def MySQLDB ():
    return instMySQLDB;

"""
if __name__ == '__main__':
    mySQLDB = MySQLDB()
    mySQLDB.createDB()
    mySQLDB.createTables()
"""
