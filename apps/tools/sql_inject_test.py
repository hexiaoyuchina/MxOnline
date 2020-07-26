import MySQLdb
username=" ' OR 1=1 #"
password=''
conn=MySQLdb.connect(host='localhost',user='root',password='123456',db='mxonline',charset='utf8')
cursor=conn.cursor()
sql="select * from users_userprofile where username='{}' and password='{}'".format(username,password)
cursor.execute(sql)
for row in cursor.fetchall():
    print(row)
