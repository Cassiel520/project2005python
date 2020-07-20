import pymysql
db=pymysql.connect(host="localhost",
                   port=3306,
                   user="root",
                   password="123456",
                   database="stu",
                   charset="utf8")
cur=db.cursor()
# with open("timg.jpeg","rb") as f:
#     data=f.read()
#     print(type(data))  #data为字节串
# sql="update cls set image=%s where id=1;"
# cur.execute(sql,data)
# db.commit()
sql="select image from cls where id=1"
cur.execute(sql)
data=cur.fetchone()  #data是元组，元组的元素是字符串
print(type(data))
with open("sp.jpeg","wb") as f:
    f.write(data[0])    #写入文档的必须是字符串，而data是元组，
cur.close()
db.close()

