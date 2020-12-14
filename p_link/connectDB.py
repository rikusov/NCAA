import pyodbc

class WorkDB(object):

    def __init__(self,server, database, user = None, password = None, driver = 'SQL Server', ac = False):
        if user is None or password is None:
            s_config = 'Driver={'+driver+'};Server='+server+';Database'+database+';Trusted_Connection=yes;'
        else:
            s_config = 'Driver={'+driver+'};Server='+server+';Database'+database+';Uid='+user+';Pwd='+password+';'
        self.conn = pyodbc.connect(s_config,autocommit=ac)
        self.cursor = self.conn.cursor()

    def Select(self,qwery):
        return self.cursor.execute(qwery).fetchall()

    def Commit_nr(self,qwery):
        self.cursor.execute(qwery)
        self.conn.commit()


def main():
    DB = WorkDB('RA19WIN10','EL','sa','60527488')
    print(DB.Select('Select * From EL.dbo.Transactions_Command_Quatter'))

if __name__ == '__main__':
    main()
