import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

host = "localhost"
user = "root"
password = "root"
root = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
)
engine = create_engine( f"mysql+mysqlconnector://{user}:{password}@{host}")
c = root.cursor()
def tableColumnParameter():
    db1, tablename = show1()
    q = f"USE {db1} "
    c.execute(q)
    q = f"DESCRIBE {tablename}"
    c.execute(q)
    column = []
    column_value = []
    placeholder = []
    for i in c.fetchall():
        if i[5] != 'auto_increment':
            column.append(i[0])
            placeholder.append('%s')
    for j in column:
        dataz = input(f"{j}=?").strip()
        if dataz == "":
            column_value.append(None)
        else:
            column_value.append(dataz)
    columnT = '(' + ','.join(column) + ')'
    placeholderT = '(' + ','.join(placeholder) + ')'
    return db1,tablename,columnT,placeholderT,column_value
def insert1():
    db1,tablename,columnT,placeholderT,column_value=tableColumnParameter()
    q=f"INSERT INTO {db1}.{tablename} {columnT} VALUES {placeholderT}"
    c.execute(q,column_value)
    root.commit()
def delete1():
    db1,tablename=show1()
    idname=input('id name=?')
    id1=int(input('id=?'))
    q=f"DELETE FROM {tablename} where {idname}={id1}"
    c.execute(q)
    root.commit()
    print('delete successfully')
def show1():
    db1 = input('ENTER THE DATABASE NAME-->')
    q=f"USE {db1}"
    c.execute(q)
    q="SHOW TABLES"
    c.execute(q)
    r=c.fetchall()
    for tb in r:
        print(tb[0])
    tablename=input("enter the table name-->")
    q=f"SELECT * FROM {db1}.{tablename}"
    df=pd.read_sql(q,engine)
    print(df)
    return db1,tablename
def showdatabase1():
    q="SHOW DATABASES"
    c.execute(q)
    result1=c.fetchall()
    for db in result1:
        print(db[0])
val=''
while val!='quit':
    val = input("choice?--> |1.insert|  |2.delete table content"
                "|  |3.show tables| |4.show databases|")
    if val=='1':
        insert1()
    elif val=='2':
        delete1()
    elif val=='3':
        show1()
    elif val=='4':
        showdatabase1()
    elif val=="quit":
        break
    else:
        print("incorrect choice ! again")
c.close()
root.close()
