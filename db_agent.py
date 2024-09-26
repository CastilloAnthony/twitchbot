import mysql
import mysql.connector

class Agent():
    def __init__(self):
        self.__cnx = None
        self.__cursor = None
    # end __init__

    def __del__(self):
        # self.__cursor.close()
        self.__cnx.close()
        del self.__cursor, self.__cnx, 
        print('Database Connection Closed.')
    # end __del__

    def connect(self, user='twitchbot', password=None, host='127.0.0.1', database='twitch'):
        try:
            if password == None:
                self.__cnx = mysql.connector.connect(
                    user=user, 
                    password=self._readPassword(),
                    host=host,
                    database=database,
                    #autocommit=True,
                )
            else:
                self.__cnx = mysql.connector.connect(
                    user=user, 
                    password=password,
                    host=host,
                    database=database,
                    #autocommit=True,
                )
            self.__cursor = self.__cnx.cursor(buffered=True, dictionary=True)
        except mysql.connector.Error as err:
            if err.errno == mysql.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access Denied, check your username and password")
            elif err.errno == mysql.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        return self.__cnx.is_connected()
    # end connect

    def _readPassword(self):
        with open('./keys/password.txt', 'r') as file:
            for line in file.readlines():
                if line != '' and len(line) > 0:
                    return line        
    # end _readToken

    def _verifyChannel(self, channel:str):
        if self.__cnx.is_connected():
            try:
                self.__cursor.execute(f'SELECT COUNT(DISTINCT username) FROM {channel}') # WIP, this is potentially greedy
                return True
            except:
                try:
                    self.__cursor.execute(f'CREATE TABLE {channel} (username VARCHAR(255) NOT NULL, creationDate DATETIME NOT NULL, lastModified DATETIME NOT NULL, cookies INT, hat VARCHAR(255), lastRoll INT, lastRolledDice VARCHAR(255), PRIMARY KEY (username));')
                    self.__cnx.commit()
                    return True
                except:
                    print('Could not create database for: ', channel)
                    return False
        else:
            print('No database is connected.')
    # end _verifyChannel

    def _checkUserExistence(self, channel:str, user:str):
        if self.__cnx.is_connected():
            self.__cursor.execute(f'SELECT username, COUNT(DISTINCT username) FROM {channel} WHERE username = "{user}";')
            result = self.__cursor.fetchone()
            if result['username'] != None:
                return True
            else:   
                self.__cursor.execute(f'INSERT INTO {channel} (username, creationDate, lastModified, cookies, hat) VALUES ("{user}", NOW(), NOW(), 100, "a nerd hat");')
                self.__cnx.commit()
                return True
        else:
            return False
    # end _checkUserExistence

    def updateDB(self, channel:str, user:str, attribute:str, rowData:str):
        if self._verifyChannel(channel):
            if self._checkUserExistence(channel, user):
                self.__cursor.execute(f'UPDATE {channel} SET lastModified = NOW(), {attribute} = "{rowData}" WHERE username = "{user}";')
                self.__cnx.commit()
                self.__cursor.execute(f'SELECT {attribute} FROM {channel} WHERE username = "{user}";')
                return self.__cursor.fetchone()
            else:
                return False
        else:
            return False
    # end updateDB

    def incrementDB(self, channel:str, user:str, attribute:str, rowData:int):
        if self._verifyChannel(channel):
            if self._checkUserExistence(channel, user):
                self.__cursor.execute(f'UPDATE {channel} SET lastModified = NOW(), {attribute} = {attribute}+{rowData} WHERE username = "{user}";')
                self.__cnx.commit()
                self.__cursor.execute(f'SELECT username, {attribute} FROM {channel} WHERE username = "{user}";')
                return self.__cursor.fetchone()[attribute]
            else:
                return False
        else:
            return False
    # end incrementDB

    def queryDB(self, channel:str, user:str, attribute:str):
        if self._verifyChannel(channel):
            if self._checkUserExistence(channel, user):
                self.__cursor.execute(f'SELECT username, {attribute} FROM {channel} WHERE username = "{user}";')
                result = self.__cursor.fetchone()
                return result
            else:
                return False
        else:
            return False
    # end queryDB
# end Agent
