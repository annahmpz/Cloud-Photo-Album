import pymysql

db = pymysql.connect("localhost", "root", "123456", "album")
cursor = db.cursor()
db.close()