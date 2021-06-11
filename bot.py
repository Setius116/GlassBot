import telebot
import usersDBrequest as udbr
import glassDBrequest as gdbr
import logsDBrequest as ldbr
import datetime as dt
#import rightsVariations as rVar

#main variables
#SetiusBot
#TOKEN = "1792700815:AAGoibW1lnzSdzOzanefMlj0Ut7uqZUbbQ8"
#GlassPhoneBot
TOKEN = "1703773972:AAF1HMODp2q6S138fx9PoUNLxPPc7pkhfU8"  

bot = telebot.TeleBot(TOKEN)
GodId=1598725425

HelpMessage = 'Наберите модель телефона для запроса.\n \t Например: samsung a50, или huawei p20.\n Так же можно использовать сокращения samsung = sam, huawei=hua, xiaomi=xia, oppo=op \n \t Пример: Sam a50 \n \n Если вы хотите добавить новую совместимость, наберите /ст и укажите обе модели. \n \t Пример: "/ст самсунг а52 подходит на нокию 3310" \n \t Эта заявка будет рассмотрена и добавлена в ближайшее время.'




def sideAnswer(message,usersList):
    for i in usersList:
        bot.send_message(i,message)

def logsAnswer(message,logs):
    bot.send_document(message.chat.id,logs)
    
        
    
def message_processing (message):
    # Запрос на права пользователя отправившего сообщение
    userRights=udbr.rightsRequest(message.from_user.id)
    #Разбивка сообщения по пробелам
    messageDetalize=message.text.split()
    # Возможные ответы незарегестрированным пользователям
    if userRights==0:
        #Если в сообщении N/A пользователя присутствует "/рег", запрос на регистрацию
        if messageDetalize[0]=='/рег':
            answer='Запрос на регистрацию отправлен. Ожидайте ответа'
            adminMessage=message.text+' '+str(message.from_user.id)
            sideAnswer(adminMessage,udbr.usersRequest([1]))
        else:
            answer='Необходимо зарегестрироватся. Для регистрации наберите "/рег *Имя фамилия* *адрес точки продаж*. Пример: /рег  Федор Пупкин Виваленд"'

    # Возможные ответы главного администратора
    if userRights==1:
        # Добавление в базу нового пользователя
        if messageDetalize[0]=='/рег':
            request=udbr.rightsRequest(int(messageDetalize[4]))
            if request!=0:
                return ('Пользователь присутствует в базе')
            else:
                try:
                    udbr.userAdd(messageDetalize)
                except:
                    return ('Неверный ввод последовательности. Верный вид команды: /рег Имя Фамилия Местоработы IdПользователя ПраваДоступа(1 или 2)')
                request=udbr.rightsRequest(int(messageDetalize[4]))
                if request!=0:
                    
                    sideAnswer('Вы были зарегестрированы, Для помощи наберите /help',[int(messageDetalize[4])])
                    return ('Пользователь добавлен в базу')
                else:
                    return('Ошибка добавления')
        # Запрос списка пользователей
        elif messageDetalize[0]=='/пользователи':
            return (udbr.usersList())
        # Удаление пользователя
        elif messageDetalize[0]=='/удалпольз':
            request=udbr.rightsRequest(int(messageDetalize[1]))
            if request!=0:
                udbr.userDelete(int(messageDetalize[1]))
                return('Пользователь удален')
            else:
                return('Пользователь отсутствует в базе. Уточните ID')
        # Запрос логов из лог базы данных
        elif messageDetalize[0]=='/лог':
            answer='База данных логов'
            logs=open('logTemp.db','r')
            logsAnswer(message,logs)
        # Отправляет в ответ файл с новыми совместимостями стекол в формате txt
        elif messageDetalize[0]=='/стеклог':
            logs=ldbr.glassAddsGet()
            if len(logs)==0:
                return ('Нет новых совместимостей')
            file=open('logTemp.txt','w')
            for i in logs:
                file.write(str(i[0])+' '+str(i[1])+' '+str(i[2])+ '\n')
            file.close()
            bot.send_document(message.chat.id,open('logTemp.txt','rb'),"logs.txt")
            return ('Список стекол на добавление')
        # Очищает базу данных новых совместимостей
        elif messageDetalize[0]=='/стеклогудал':
            ldbr.glassAddsDelete()
            return ('все запросы на добавление стекол удалены')
            
        # Добавление стекла в базу данных
        #elif messageDetalize[0]=='/добстекло':
            #if len(messageDetalize)>=4:
                #answer=udbr.glassAdd(messageDetalize[1],messageDetalize[2:-1],messageDetalize[-1])

    # Для всех пользователей (Права пользователя от 1 до 3)
    if userRights>=1:
        if messageDetalize[0][0]!='/':
            if len(messageDetalize)>=2:
                if len(messageDetalize)>=3:
                    model=''
                    for i in range(1,len(messageDetalize)):
                        model+=messageDetalize[i]
                else:
                    model=messageDetalize[1]
                            
                answer=gdbr.CompatibilityModelsFinder(messageDetalize[0],model)
                return (answer)
            else:
                answer='Ошибка.Неверный ввод'
        elif messageDetalize[0]=='/ст':
            date=dt.datetime.fromtimestamp(message.date)
            user=udbr.usersNameRequest(message.from_user.id)
            text=message.text[3:-1]
            answer=ldbr.glassAddRequest(date,user[0][0],text)
            sideAnswer('Новое стекло на добавление',udbr.usersRequest([1]))
            return (answer)
        elif messageDetalize[0]=='/help':
            return (HelpMessage)
                            
            
            
            

     # Права пользователей уровня менеджер и ниже           
     #if userRights>=2:
         #if messageDetalize[0]=='/добстекло':
             
        
        
            


        else:
            answer='Неверная команда'

            
                                       
            
    return (answer)


@bot.message_handler(content_types=['text'])

#Делает запрос в обработчик сообщений и отвечает пользователю результат
def start_handler(message):
    try:
        answer=message_processing(message)
        bot.send_message(message.chat.id, answer)
        #Заносит данные о сообщение и ответ в базу данных логов
        ldbr.logAdd(message,answer)
    except:
        pass
    
    
    
bot.polling()



