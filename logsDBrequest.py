import sqlite3
import datetime as dt
import usersDBrequest as udbr


def logAdd (message,answer):
    time=str(dt.datetime.fromtimestamp(message.date))
    userId=str(message.from_user.id)
    request=udbr.rightsRequest(int(userId))
    if request!=0:
        userData=udbr.userForId(int(userId))
        userName=userData[0]
        userWorkplace=userData[3]
    else:
        userName='N/A'
        userWorkplace='N/A'
    userRequest=message.text
    answerText=answer
    
    conn=sqlite3.connect('logsDB.db')
    cur=conn.cursor()
    cur.execute("INSERT INTO logs VALUES(?,?,?,?,?,?)",(time,userId,userName,userWorkplace,userRequest,answerText))
    conn.commit()
    conn.close()
# возвращает данные из базы данных на добавление совместимых стекол
def glassAddsGet():
    conn=sqlite3.connect('glassAdd.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM addRequests")
    text=cur.fetchall()
    return (text)

# Зачищает базу данных новых запросов на совместимость стекол
def glassAddsDelete():
    conn=sqlite3.connect('glassAdd.db')
    cur=conn.cursor()
    cur.execute("DELETE FROM addRequests")
    conn.commit()
    conn.close()
    
def glassAddRequest(date,userName,text):
    conn = sqlite3.connect('glassAdd.db')
    cur=conn.cursor()
    cur.execute("INSERT INTO addRequests VALUES(?,?,?)",(date,userName,text))
    conn.commit()
    conn.close()
    return ('Запрос добавлен и будет рассмотрен администрацией')
    
    
        
    
