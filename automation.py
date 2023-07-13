# Import libraries required for connecting to mysql
import mysql.connector
# Import libraries required for connecting to DB2
import ibm_db
# Connect to MySQL
connection = mysql.connector.connect(user='root', password='******',host='127.0.0.1',database='sales')

# create cursor
cursor = connection.cursor()

# Connect to DB2
dsn_hostname = "***.databases.appdomain.cloud"
dsn_uid = "***"       
dsn_pwd = "***"
dsn_port = "32304" 
dsn_database = "bludb"    
dsn_driver = "{IBM DB2 ODBC DRIVER}"        
dsn_protocol = "TCPIP"     
dsn_security = "SSL"     

    #Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

    # create connection
conn = ibm_db.connect(dsn, "", "")


# The function get_last_rowid returns the last rowid of the table sales_data on the IBM DB2 database.

def get_last_rowid():
	
    SQL1 = """select max(ROWID) from sales_data"""
    last_rowid = ibm_db.exec_immediate(conn, SQL1)
    while ibm_db.fetch_row(last_rowid) != False:
        return ibm_db.result(last_rowid, 0)

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)


# The function get_latest_records returns a list of all records from MySQL that have a rowid greater than the last_row_id 
# in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    SQL = """SELECT
        rowid,
        product_id,
        customer_id,
        '0' as price,
        quantity,
        now()
    from sales_data
    where rowid > {}""".format(rowid)
    cursor.execute(SQL)
    return cursor.fetchall()

new_records = get_latest_records(last_row_id)
print("New rows on staging datawarehouse = ", len(new_records))


# The function insert_records inserts all the records passed to it into the sales_data table in IBM DB2 database.

def insert_records(records):
    SQL = "INSERT INTO sales_data(rowid,product_id,customer_id,price,quantity,timestamp) VALUES(?,?,?,?,?,?);"
    stmt = ibm_db.prepare(conn, SQL)
    for row in new_records:
        ibm_db.execute(stmt, row)
        return 1

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
connection.close()
# disconnect from DB2 data warehouse
ibm_db.close(conn)

