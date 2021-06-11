import sqlite3

# Делает запрос в базу пользователей и возвращает графу Права пользователей
def rightsRequest (Id):
    conn = sqlite3.connect('usersBase.db')
    cur=conn.cursor()
    cur.execute("SELECT userRights FROM Users WHERE userID=?",(Id,))
    requestResult=cur.fetchall()
    conn.close()
    if len(requestResult)!=0:
        return (requestResult[0][0])
    else:
        return (0)
#Возвращает список пользователей с указанными правами
def usersRequest (rightsList):
    Id=[]
    for i in rightsList:
        conn = sqlite3.connect('usersBase.db')
        cur=conn.cursor()
        cur.execute("SELECT userID FROM Users WHERE userRights=?",(i,))
        users=cur.fetchall()
        for j in users:
            Id.append(j[0])
        conn.close()
    return (Id)
# возвращает имя пользователя по id
def usersNameRequest(Id):
    conn=sqlite3.connect('usersBase.db')
    cur=conn.execute("SELECT userName FROM Users WHERE userID=?", (Id,))
    userName=cur.fetchall()
    return (userName)
#Добавляет в базу нового пользователя
def userAdd (data):
    userName=data[1]+' '+data[2]
    conn=sqlite3.connect('usersBase.db')
    cur=conn.cursor()
    cur.execute("INSERT INTO Users VALUES(?,?,?,?)",(userName,int(data[4]),int(data [5]),data[3]))
    conn.commit()
    conn.close()


#Возвращает список пользователей одной строкой
def usersList ():
    con=sqlite3.connect('usersBase.db')
    cur=con.cursor()
    cur.execute("SELECT * FROM Users")
    users=cur.fetchall()
    userList=''
    for i in users:
        Id=i[1]
        #stroke='Имя: '+i[0]+', '+'Место: '+i[3]+', '+'ID: %d , '+'Права: '+str(i[2])+'\n' % (i[1],)
        stroke='Имя: %s, Место: %s, ID: %d , Права: %s \n' % (i[0],i[3],i[1],str(i[2]),)
        userList+=stroke+'\n'
    
    return (userList)
#Удаляет пользователя по Id
def userDelete(Id):
    conn=sqlite3.connect('usersBase.db')
    cur=conn.cursor()
    cur.execute("DELETE FROM Users WHERE userID = ?",(Id,))
    conn.commit()
    conn.close()

# Возвращает данные о пользователе по Id
def userForId(Id):
    con=sqlite3.connect('usersBase.db')
    cur=con.cursor()
    cur.execute("SELECT * FROM Users WHERE userID=?",(Id,))
    users=cur.fetchall()
    return (users[0])


    
    
    
    
    
        
