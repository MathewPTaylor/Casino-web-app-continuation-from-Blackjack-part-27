import sqlite3


class DBFuncs:
    data_types = ["text", "integer", "real", "boolean", "blob"]
    
    def __init__(self, dbfilename: str):
        self.dbFileName = dbfilename
        self.fields = []
        self.tableName = ""
        self.primaryKey = ""
        # making db file
        conn = sqlite3.connect(self.dbFileName)
        conn.close()  
    def addTable(self, tablename):
        assert len(self.fields) > 0

        # connecting to the database
        conn = sqlite3.connect(self.dbFileName)

        # adding a cursor
        cursor = conn.cursor()

        print(f"CREATE TABLE {tablename} ({''.join(f'{field[0]} {field[1]}, ' for field in self.fields)[:-2]})")

        # executing SQL statement
        cursor.execute(f"CREATE TABLE {tablename} ({''.join(f'{field[0]} {field[1]}, ' for field in self.fields)[:-2]})")

        # committing changes
        conn.commit()

        # Close connection
        conn.close()
        

    def addField(self, fieldname: str, datatype: str, isprimarykey: bool=False):
        if datatype not in self.__class__.data_types:
            raise Exception("Invalid Data type ('{}')".format(datatype))
        else:
            if fieldname not in [field[0] for field in self.fields]:
              self.fields.append((fieldname, datatype))
              if isprimarykey:
                  self.primaryKey = fieldname
            else:
              print("Field already exists ('{}')".format(fieldname))

    def addRecord(self, *fieldvals):
        # connect to database
        conn = sqlite3.connect(self.dbFileName)

        # create cursor
        cursor = conn.cursor()

        print(fieldvals, type(fieldvals))
        print(f"INSERT INTO {self.tablename} VALUES ({self.__FormatFieldParam()})")
        print(self.__autoMakeDictArg(fieldvals))

        # execute SQL statement
        cursor.execute(f"INSERT INTO {self.tablename} VALUES ({self.__FormatFieldParam()})", self.__autoMakeDictArg(fieldvals))

        # commit changes
        conn.commit()

        # close connection
        conn.close()


    def FetchAllRecords(self):
        # Connect to database
        conn = sqlite3.connect(self.dbFileName)

        # Create cursor (cursors operate on the database)
        cursor = conn.cursor()

        # Execute the SQL statement to get all the records
        cursor.execute(f"SELECT * FROM {self.tablename}")

        # Storing the fetched data into a variable
        records = cursor.fetchall()

        # Committing changes (we're not really changing anything, but it's good to just commit any ways)
        conn.commit()

        # Close the connection with the database
        conn.close()

        return records

    def addTableName(self, tablename):
        self.tablename = tablename

    @staticmethod
    def UpdateRecord(self, record):
      # Create the database or connect to it
      conn = sqlite3.connect(self.dbFileName)

      # Create cursor (cursors operate on the database)
      cursor = conn.cursor()

      #print("DB KEYS:", db.keys())
      # Execute the SQL statement to update the player's info in the database
      #cursor.execute()

      tostr = ""
      # one field will be [<fieldname>, <fieldvalue>]
      for field in record:
        tostr += f"{field[0].upper()}='{field[1]}', "
      print(tostr)
      # Close Connection
      conn.close()
      

    def deleteAllRecords(self):
        # Connect to database
        conn = sqlite3.connect(self.dbFileName)

        # Create cursor (cursors operate on the database)
        cursor = conn.cursor()

        # Execute the SQL statement to get all the records
        cursor.execute(f"DELETE FROM {self.tablename}")

        # Committing changes
        conn.commit()

        # Close the connection with the database
        conn.close()


    def deleteRecord(self, primarykeyvalue):
        # Connect to database
        conn = sqlite3.connect(self.dbFileName)

        # Create cursor (cursors operate on the database)
        cursor = conn.cursor()

        # Execute the SQL statement to get all the records
        cursor.execute(f"SELECT * FROM {self.tablename} WHERE {self.primaryKey} = '{primarykeyvalue}'")

        # Committing changes
        conn.commit()

        # Close the connection with the database
        conn.close()


    def __autoMakeDictArg(self, fieldvals) -> dict:
        dict_arg = {}
        for i in range(len(self.fields)):
            dict_arg[self.fields[i][0]] = fieldvals[i]
        return dict_arg

    
    def __FormatFieldParam(self) -> str:
        return "".join(f":{field[0]}, " for field in self.fields)[:-2]




