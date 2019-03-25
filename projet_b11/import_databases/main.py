import mysql.connector
from ThreeDid import ThreeDid

# init mysql connection
try:
    cnx = mysql.connector.connect(user='root', host='localhost')
    cur = cnx.cursor()
except mysql.connector.Error as e:
    print(e)

did = ThreeDid()
#did.get_version()
#print(did.version)
#did.get_db()
did.import_db(cur)
#did.test_db(cur)

cnx.close()
cur.close()
