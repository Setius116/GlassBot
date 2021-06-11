import sqlite3
import re

# Конфигурирует 



#Добавляет модель в базу
def glassAdd(brend,modelName,modelType):
    brend=brend.lower()
    brend=brend.capitalize()
    if (brend!='Samsung' and
        brend!='Huawei' and
        brend!='Xiaomi'):
        if brend=='Sam':
            brend='Samsung'
        elif brend=='Hua':
            brend='Huawei'
        elif brend=='Xia':
            brend='Xiaomi'
        elif brend== 'Op':
            brend = 'Oppo'
        else:
            return ('Ошибка наименования бренда')
    
    conn=sqlite3.connect('modelBase.db')
    cur1=conn.cursor()
    cur1.execute("SELECT Id FROM glass WHERE brand=?",(brend,))
    number=cur1.fetchall()
    number=[i[0] for i in number]
    number=number[-1]+1
    
    model=''
    for i in modelName:
        model+=i
    modelType=int(modelType)
    cur1.execute("INSERT INTO glass VALUES(?,?,?,?,?,?)",(number,brend,model,None,None,modelType))
    conn.commit()
    conn.close()
    answer="Стекло добавлено в базу. %s %s, %s"% (brend,model,str(modelType))
    
    return (answer)
    

# Ищет модель в базе моделей. Если таковой нет выводит возможные варианты.
#если нет вариантов, выводит сообщение об отсутствии.
def CompatibilityModelsFinder(brend,model):
    brend=brend.lower()
    brend=brend.capitalize()
    if (brend!='Samsung' and
        brend!='Huawei' and
        brend!='Xiaomi'):
        if brend=='Sam':
            brend='Samsung'
        elif brend=='Hua':
            brend='Huawei'
        elif brend=='Xia':
            brend='Xiaomi'
        elif brend=='Op':
            brend='Oppo'
        else:
            return ('Ошибка наименования бренда')

    conn = sqlite3.connect('modelBase.db')
    #Обьявляем два курсора
    cur1 = conn.cursor()
    cur2 = conn.cursor()
    cur3 = conn.cursor()

    #В первый курсор берем столбец "models"
    #отсортированнные по столбцу "brand"
    cur1.execute("SELECT models FROM glass WHERE brand=?",(brend,))
    #cur1.execute("SELECT models FROM glass WHERE brand=?", brand)
    #Во второй курсор берем столбец "GlassId"
    #отсортированнные по столбцу "brand"     
    #cur2.execute("SELECT GlassId FROM glass WHERE brand=?", (brend,))
    cur2.execute("SELECT Id FROM glass WHERE brand=?",(brend,))

    #Создаем список моделей
    models=[]
    #Цикл заполнения списка моделей взятых из cur 1
    for i in cur1.fetchall():
        #преобразоввываем dict в строку
        unit=i[0]
        #убираем пробелы из строки
        unit=''.join([i for i in unit if i!=' '])
        #понижаем весь регистр в строке
        unit=unit.lower()
        #добавляем строку в список
        models.append(unit)
    #Убираем пробелы из строки модели
    modelLow=''.join([i for i in model if i!=' '])
    
    #понижаем регистр в строке модели
    modelLow=modelLow.lower()
    #ищем совпадение model в списке models возвращаем индекс
    # если есть совпадение в моделях то
    if models.count(modelLow) !=0:
        
        Id=cur2.fetchall()[models.index(modelLow)][0]
        

        cur1.execute ("SELECT GlassId1, GlassId2,GlassId3,GlassId4 FROM glass WHERE Id=?",(Id,))       
        
        GlassIdList=[i for i in cur1.fetchall()[0] if i!=None]
        modelsList=[]
        for i in GlassIdList:
            cur1.execute ("SELECT brand, models, GlassId1, GlassId2, GlassId3, GlassId4 FROM glass WHERE GlassId1=? or GlassId2=? or GlassId3=? or GlassId4=?",(i,i,i,i,))
            List=cur1.fetchall()
            for i in List:
                if modelsList.count([i[0],i[1]])==0:
                    modelsList.append([i[0],i[1]])
                if i[2]!=None:
                    if GlassIdList.count(i[2])==0:
                        GlassIdList.append(i[2])
                if i[3]!=None:
                    if GlassIdList.count(i[3])==0:
                        GlassIdList.append(i[3])
                if i[4]!=None:
                    if GlassIdList.count(i[4])==0:
                        GlassIdList.append(i[4])
                if i[5]!=None:
                    if GlassIdList.count(i[5])==0:
                        GlassIdList.append(i[5])
            List=None

        modelsList.sort()
        result='Возможные совместимые модели:\n'
        for i in range (0,len(modelsList)):
            result=result+str(i+1)+') '+str(modelsList[i][0])+' '+str(modelsList[i][1])+'\n'
        
    else:
        
        findModel=model.split(' ')
        maybeModels=[]
        for i in models:
            if re.search(findModel[-1],i):
                maybeModels.append(i)
        if len(maybeModels)!=0:
            result='Модель не найдена. Возможно вы имели ввиду :\n'
            for i in maybeModels:
                result+=i+'\n'
            result+='Введите модель правильно'
        else:
            result='Модель в базе не обнаружена'
    conn.close()
            
                
    return (result)

def GlassIdLast():
    conn=sqlite3.connect('modelBase.db')
    cur1=conn.cursor()
    cur1.execute("SELECT GlassId1, GlassId2,GlassId3,GlassId4 FROM glass")   




