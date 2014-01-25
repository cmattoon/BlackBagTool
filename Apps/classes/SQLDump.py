"""
This class is used to dump sqlite3 databases into CSV files
"""
import os, sqlite3, csv

class SQLDump:
    def __init__(self, db_filepath):
        # Let someone else handle exceptions.
        self.db = sqlite3.connect(db_filepath)
        
    def getTables(self):
        tbls = []
        try:
            c = self.db.cursor()
            for row in c.execute('SELECT tbl_name FROM sqlite_master WHERE type="table"'):
                tbls.append(row[0].encode('UTF-8'))
        except:
            pass

        return tbls
        

    def getColumns(self, tbl):
        cols = []
        try:
            c = self.db.cursor()
            for row in c.execute('SELECT * FROM %s LIMIT 1' % tbl):
                for coldata in c.description:
                    cols.append(coldata[0])
        except:
            pass
        return cols

    def getCSV(self, tbl, outfile):
        data = []
        header = []
        try:
            c = self.db.cursor()
            for row in c.execute('SELECT * FROM %s' % tbl):
                data.append(row)
                if len(header) == 0:
                    for tup in c.description:
                        header.append(tup[0])

            with open(outfile,'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(header)
                for row in data:
                    writer.writerow(row)
            return True
        except:
            return False

    
