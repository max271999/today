from telebot import TeleBot, types
import json
# from telebot.states import stateGroup, state

BOT_TOKEN = "6093650930:AAHjesG87iPoPjcEPJk7BLtjfKU09QOKWf0"
bot = TeleBot(BOT_TOKEN)


#funksiyalar 

#majburiy obunani tekshirish funksiyasi
def Checksub(msg):
    with open("data.json", "rb") as f:
        data = json.load(f)
    user = []
    for channel in data["kanallar"]:
        try:

            checkuser = bot.get_chat_member(f"@{channel}", msg.from_user.id).status

            if checkuser in ["member", "administrator", "creator"]:
                continue
            else:
                user.append(channel)
        except:
            bot.send_message(data['ega'],f"{channel} kanalida xatolik bor")

    checksubbtns = types.InlineKeyboardMarkup(row_width=1)
    if len(user) == 1:
        checksubbtns.add(types.InlineKeyboardButton(text=f"{user[0].title()}", url=f"https://t.me/{user[0]}"))
        checksubbtns.add(types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="checksub"))
        bot.send_message(msg.from_user.id,"ushbu kanalga obuna bo'lgandan so'ng botni ishlatishingiz mumkin!",reply_markup=checksubbtns)
    elif len(user) > 1:
        for channel in user:
            button = types.InlineKeyboardButton(text=f"{channel.title()}", url=f"https://t.me/{channel}")
            checksubbtns.add(button)
        checksubbtns.add(types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="checksub"))
        bot.send_message(msg.from_user.id,"ushbu kanallarga obuna bo'lgandan so'ng botni ishlatishingiz mumkin!",reply_markup=checksubbtns)
    else:
        return True

#adminlar start bosganida yuboriladigan xabar
def vote(msg):
    with open("data.json","r") as f:
        data = json.load(f)
    try:
        buttons = types.InlineKeyboardMarkup(row_width=1)
        # admin start bosganida ko'rinadigan tugmalar
        if str(msg.from_user.id) in data['adminlar'].keys():
            admin_button = types.InlineKeyboardButton(text="Bot malumotlarini tahrirlash",callback_data="edit_info")
        if str(msg.from_user.id) == data["ega"]:
            ega_button = types.InlineKeyboardButton(text="adminlar", callback_data="edit_admin")
            buttons.add(ega_button)
        buttons.add(admin_button)
        return buttons

    except :
        bot.send_message(data['ega'],"nomzodlarni haqida malumotda xatolik bor")
    #nomzodlar tugmalari malumotlari


#adminlar botni tahrirlash uchun bo'lim
def EditBotBtns():

    editbtns = types.InlineKeyboardMarkup(row_width=1)
    editbtns.add(
        types.InlineKeyboardButton(text="Majburiy obunaga kanal qo'shish",callback_data="addchannel"),
        types.InlineKeyboardButton(text="Majburiy obunadan kanalni olib tashlash",callback_data="removechannel"),
        types.InlineKeyboardButton(text="ovoz yig'ish", callback_data="nomzodlar"),
        types.InlineKeyboardButton(text="kanallarga reklama yuborish", callback_data="reklama"),
        types.InlineKeyboardButton(text="botdan foydalanuvchilarga xabar jo'natish",callback_data="senduser"),
        types.InlineKeyboardButton(text="Premium foydalanuvchilarga xabar jo'natish", callback_data="sendpremiumuser"),
    )
    return editbtns


#foydalanuvchi haqida malumot
def userinfo(msg):
    try:
        with open("data.json","r") as f:
            data = json.load(f)
        user_info = {
            "id": msg.from_user.id,
            "username": msg.from_user.username,
            "premium": msg.from_user.is_premium
        }

        with open('data.json', 'w') as file:
            data["users"][str(msg.from_user.id)] = user_info
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"{msg.from_user.username} foydalanuvchisini malumotlarini saqlashni iloji bo'lmadi bo'lmadi: {e}")

def useradmin(msg):
    """msg habar qabul qilib xabar yuboruvchi admin ekanligini tasdiqlaydi"""
    with open("data.json","rb") as f:
        data = json.load(f)

    if str(msg.from_user.id) in data["adminlar"] or str(msg.from_user.id) == data["ega"]:
        return True
    else:
        return False


#nomzodlar tugmalari
def Nomzodlarbtn():
    """json faylidagi nomzodlarni tugmalarga joylab beradi ovozlar sonini ko'rsatadi"""
    with open("data.json","rb") as f:
        data = json.load(f)
    nomzodlarbtn = types.InlineKeyboardMarkup(row_width=1)
    for nomzod in data["nomzodlar"]:
        ovozlar = 0
        for ovoz in data["ovozlar"].values():
            if nomzod == ovoz:
                ovozlar += 1
        nomzodlarbtn.add(types.InlineKeyboardButton(text=f"{nomzod} || {ovozlar}",callback_data=nomzod))
    return nomzodlarbtn







#botga start bosilganida bajariladigan amal
@bot.message_handler(commands=['start','help'])
def start_message(msg: types.Message):

    userinfo(msg)

    if useradmin(msg):
        with open("img/admin.jpg","rb") as img:
            img = img
            bot.send_photo(msg.from_user.id,img,caption="Bot admin paneliga xush kelibsiz!",reply_markup=vote(msg))




#inline tugmalar bosilganida bajariladigan amallar
@bot.callback_query_handler(func=lambda x: x.data)
def query(msg: types.CallbackQuery):
    with open("data.json","rb") as f:
        data = json.load(f)
    
    userinfo(msg)

    match msg.data:
        case "nomzodlar":
            bot.send_message(msg.from_user.id,"nomzodlarni bittalab kiriting!")
            data["addnomzodlar"] = str(msg.from_user.id)
            data["nomzodlar"] = []
            with open("data.json","w") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        case "nomzodlartayyor":
            bot.send_message(msg.from_user.id,"Ovoz yig'ish posti uchun matn kiriting, foydalanish taqiqlanadi (emoji,stiker). \nmatnni etibor bilan yozing!!!")
            data['addnomzodlar'] = ""
            data["nomzodlartext"] = "edit"
            with open("data.json","w") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        case "edit_info":
            bot.send_message(msg.from_user.id,"botdan foydalanish",reply_markup=EditBotBtns())
        case "sendvotechannel":
            buttons = types.InlineKeyboardMarkup(row_width=1)
            for kanal in data["kanallar"]:
                buttons.add(types.InlineKeyboardButton(text=f"{kanal}", callback_data=f"sendvote{kanal}"))
            buttons.add(types.InlineKeyboardButton(text="hammasiga yuborish",callback_data="sendvoteallchannel"))
            bot.send_message(msg.from_user.id,"qaysi kanallarga yuborish kerakligini tanlang",reply_markup=buttons)
    # ovoz yig'ish postini kanalga yuklash
        case "sendvoteallchannel":
            try:
                for kanal in data["kanallar"]:
                    buttons = types.InlineKeyboardMarkup(row_width=1)
                    for k in data["nomzodlar"]:

                        # oddiy foydalanuvchi start bosganida ovozlarni ko'rsatish
                        ovozlar_soni = 0
                        for id, ovoz in data["ovozlar"].items():
                            if k == ovoz:
                                ovozlar_soni += 1
                        button = types.InlineKeyboardButton(text=f"{k} || ({ovozlar_soni})",
                                                            callback_data=k)
                        buttons.add(button)
                    img = data["rasm"]
                    bot.send_photo(f"@{kanal}",img , caption=data["nomzodlartext"], reply_markup=buttons)
            except:
                pass
    for kanal in data['kanallar']:
        if msg.data == f"sendvote{kanal}":
            buttons = types.InlineKeyboardMarkup(row_width=1)
            for k in data["nomzodlar"]:
                # oddiy foydalanuvchi start bosganida ovozlarni ko'rsatish
                ovozlar_soni = 0
                for id, ovoz in data["ovozlar"].items():
                    if k == ovoz:
                        
                        ovozlar_soni += 1
                if len(data["ovozlar"].values()) == 0 or ovozlar_soni == 0:
                    foyiz = 0
                else:
                    foyiz = int(ovozlar_soni / len(data["ovozlar"].values()) * 100)
                button = types.InlineKeyboardButton(text=f"{k} || {ovozlar_soni} [{foyiz}%]",
                                                    callback_data=k)
                buttons.add(button)
            img = data["rasm"]
            bot.send_photo(f"@{kanal}", img, caption=data["nomzodlartext"], reply_markup=buttons)
        #ovozni yig'ish 
        
        if msg.data in data["nomzodlar"]:
            if str(msg.from_user.id) not in data["ovozlar"].keys():
                bot.answer_callback_query(msg.id,text="ovoz berildi!")
                data["ovozlar"][msg.from_user.id] = msg.data
                with open("data.json","w") as f:
                    json.dump(data,f,indent=4,ensure_ascii=False)

                buttons = types.InlineKeyboardMarkup(row_width=1)
                for k in data["nomzodlar"]:

                    # oddiy foydalanuvchi start bosganida ovozlarni ko'rsatish
                    ovozlar_soni = 0
                    for id, ovoz in data["ovozlar"].items():
                        if k == ovoz:
                            ovozlar_soni += 1
                    
                    if len(data["ovozlar"].values()) == 0 or ovozlar_soni == 0:
                        foyiz = 0
                    else:
                        foyiz = int(ovozlar_soni / len(data["ovozlar"].values()) * 100)
                    button = types.InlineKeyboardButton(text=f"{k} || {ovozlar_soni}  [{foyiz}%]",callback_data=k)
                    buttons.add(button)
                bot.edit_message_reply_markup(
                    chat_id=msg.message.chat.id,
                    message_id=msg.message.message_id,
                    reply_markup=buttons
                    )

            else:
                bot.answer_callback_query(msg.id,text="siz allaqachon ovoz berdingiz!")
                
                
            
            
            



@bot.message_handler()
def send_admin(msg: types.Message):
    with open("data.json","rb") as f:
        data = json.load(f)

    userinfo(msg)
    
    if useradmin(msg):
        
        
        #nomzodlarni tahrirlash
        if str(msg.from_user.id) == data["addnomzodlar"]:
            try:
                data["nomzodlar"].append(msg.text)
                with open("data.json","w") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                buttons = Nomzodlarbtn()
                buttons.add(
                    types.InlineKeyboardButton(text="Tayyor", callback_data="nomzodlartayyor")
                )
                
                bot.send_message(msg.from_user.id,data["nomzodlartext"],reply_markup=buttons)
            except:
                bot.send_message(msg.from_user.id,"xato malumot yuborildi. ortiqcha belgilardan foydalanman. \n\ndasturchiga xabar berildi!!")
                bot.send_message(data["developer"],f"nomzodlarni qo'shishda xatolik bo'ldi ({msg.text})")
        elif str(msg.from_user.id) == data["nomzodlartext"]:
            try:
                data["nomzodlartext"] = msg.message_id
                data["rasm"] = "send"
                with open("data.json","w") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                bot.send_message(msg.from_user.id,"post uchun rasm jo'nating!")
            except:
                bot.send_message(msg.from_user.id,"xato malumot yuborildi. ortiqcha belgilardan foydalanman. \n\ndasturchiga xabar berildi!!")
                bot.send_message(data["developer"],f"nomzodlarni qo'shishda xatolik bo'ldi ({msg.text})")
        

#admin saylov malumotlarini o'zgartirganidan so'ng saylov uchun matn
@bot.message_handler(content_types=['photo'])
def send_photo(msg: types.Message):
    with open("data.json","rb") as f:
        data = json.load(f)
    if useradmin(msg):
        if "send" == data["rasm"]:
            file_id = msg.photo[-1].file_id
            data['rasm'] = file_id
            with open("data.json","w") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            buttons = Nomzodlarbtn()
            buttons.add(types.InlineKeyboardButton(text='kanalga uzatish➡️',callback_data="sendvotechannel"))
            
            bot.send_photo(msg.from_user.id,file_id,caption=data["nomzodlartext"], reply_markup=buttons)
            
            
#Omonqoʻtan
#
#Qorabuloq
#
#Qoratepa
#
#Terak
#
#Beshyogʻoch
#
#Moʻminobod
#
#Chep
#
#Tinchlik
#
#Beshkapa
#
#Gulobod
#
#Kamongaron
#
#Oqmachit
#
#Ispanza 
#
#Goʻslik
#
#Torinjak
#
#Kamardon
#
#Navbogʻ
#
#Doʻstlik 
#
#Navroʻz
#
#Soʻfiyon
#
#Kalangar
            
            
    




bot.polling(timeout=60)