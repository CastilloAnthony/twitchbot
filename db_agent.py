import mysql
import mysql.connector

class Agent():
    def __init__(self) -> None:
        self.__cnx = None
        self.__cursor = None
    # end __init__

    def __del__(self) -> None:
        # self.__cursor.close()
        self.__cnx.close()
        del self.__cursor, self.__cnx, 
        print('Database Connection Closed.')
    # end __del__

    def connect(self, user='twitchbot', password=None, host='127.0.0.1', database='twitch') -> bool:
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

    def _readPassword(self) -> str:
        with open('./keys/password.txt', 'r') as file:
            for line in file.readlines():
                if line != '' and len(line) > 0:
                    return line        
    # end _readToken

    def _verifyChannel(self, channel:str) -> bool:
        if self.__cnx.is_connected():
            try:
                self.__cursor.execute(f'SELECT COUNT(DISTINCT username) FROM {channel}') # WIP, this is potentially greedy
                return True
            except:
                try:
                    self.__cursor.execute(f'CREATE TABLE {channel} (id INT NOT NULL, username VARCHAR(255) NOT NULL, creationDate DATETIME NOT NULL, lastModified DATETIME NOT NULL, cookiesRewardTime DATETIME, cookies INT, hat VARCHAR(255), lastRoll INT, lastRolledDice VARCHAR(255), PRIMARY KEY (id));')
                    self.__cursor.execute(f'CREATE TABLE quotes_{channel} (id INT NOT NULL AUTO_INCREMENT, quote TEXT NOT NULL, PRIMARY KEY (id))')
                    self.__cnx.commit()
                    return True
                except:
                    print('Could not create database for: ', channel)
                    return False
        else:
            print('No database is connected.')
            return False
    # end _verifyChannel

    def _checkUserExistence(self, channel:str, id:int, user:str) -> bool:
        if self.__cnx.is_connected():
            self.__cursor.execute(f'SELECT username, COUNT(DISTINCT username) FROM {channel} WHERE id = {id};')
            result = self.__cursor.fetchone()
            if result['username'] != None:
                return True
            else:   
                self.__cursor.execute(f'INSERT INTO {channel} (id, username) VALUES ({id}, "{user}");')
                self.__cnx.commit()
                return True
        else:
            return False
    # end _checkUserExistence

    def updateDB(self, channel:str, id:int, user:str, attribute:str, rowData:str) -> bool | dict:
        if self._verifyChannel(channel):
            if self._checkUserExistence(channel, id, user):
                self.__cursor.execute(f'UPDATE {channel} SET lastModified = NOW(), {attribute} = "{rowData}" WHERE id = {id};')
                self.__cnx.commit()
                self.__cursor.execute(f'SELECT {attribute} FROM {channel} WHERE id = {id};')
                return self.__cursor.fetchone()
            else:
                return False
        else:
            return False
    # end updateDB

    def incrementDB(self, channel:str, id:int, user:str, attribute:str, rowData:int) -> bool | dict:
        if self._verifyChannel(channel):
            if self._checkUserExistence(channel, id, user):
                self.__cursor.execute(f'UPDATE {channel} SET lastModified = NOW(), {attribute} = {attribute}+{rowData} WHERE id = {id};')
                self.__cnx.commit()
                self.__cursor.execute(f'SELECT username, {attribute} FROM {channel} WHERE id = {id};')
                return self.__cursor.fetchone()[attribute]
            else:
                return False
        else:
            return False
    # end incrementDB

    def queryDB(self, channel:str, id:int, user:str, attribute:str) -> bool | dict:
        if self._verifyChannel(channel):
            if self._checkUserExistence(channel, id, user):
                self.__cursor.execute(f'SELECT username, {attribute} FROM {channel} WHERE id = "{id}";')
                result = self.__cursor.fetchone()
                return result
            else:
                return False
        else:
            return False
    # end queryDB

    def addQuote(self, channel:str, quote:str) -> bool:
        if quote != None:
            if len(quote) > 0:
                self.__cursor.execute(f'INSERT INTO quotes_{channel} (quote) VALUES ("{quote}");')
                self.__cnx.commit()
                return True
            else:
                return False
        else:
            return False
    # end addQuote

    def getQuote(self, channel:str, number:int) -> str | bool:
        if self._verifyChannel(channel):
            if number != None:
                self.__cursor.execute(f'SELECT quote FROM quotes_{channel} WHERE id="{number}";')
                result = self.__cursor.fetchone()
                return result
            else:
                return False
        else:
            return False
    # end getQuote

    def getQuoteCount(self, channel:str) -> int | bool:
        if self._verifyChannel(channel):
            self.__cursor.execute(f'SELECT COUNT(DISTINCT id) AS numberOfQuotes FROM quotes_{channel};')
            result = self.__cursor.fetchone()['numberOfQuotes']
            return result
        else:
            return False
# end Agent