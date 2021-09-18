from pyrogram import Client, filters
from pyrogram.types import MessageEntity
import tgcrypto 

#get telegram account access

bot = Client("NICSriLankaBot", config_file = "config.ini")

#start command

@bot.on_message(filters.command(commands = ["start"]))
def welcome(client, message):
    message.reply_text(text = """Hi Welcome...
I'm @NICSriLankaBOT
I can calculate birthday with new and old NIC numbers.

Enter NIC Number...""")

#get correct id

@bot.on_message(filters.text)
def start(client, message):
    def check_id():
        while True:
            id_number = (message.text).upper()
            if len(id_number) == 12:
                if (0 < int(id_number[4:7]) < 366 or 0 < int(id_number[4:7]) - 500 < 366) and 1900 < int(id_number[0:4]) < 2004:
                    return id_number, int(id_number[0:4]), int(id_number[4:7])
                else:
                    message.reply_text("Please check your NIC number and Enter again...")
                    return "None"
            elif len(id_number) == 10:
                if "V" in id_number[9]:
                    if 0 < int(id_number[2:5]) < 366 or 0 < int(id_number[2:5]) - 500 < 366:
                        return id_number, int("19" + id_number[0:2]), int(id_number[2:5])
                    else:
                        message.reply_text("Please check your NIC number and Enter again...")
                        return "None"
                else:
                    message.reply_text("Please check your NIC number and Enter again...")
                    return "None"
            else:
                message.reply_text("Please check your NIC number and Enter again...")
                return "None"

    id_year_days = check_id()
    id_number = id_year_days[0]

    if id_year_days != "None":
        year = id_year_days[1]
        days = id_year_days[2]

        #check gender

        if days < 500:
            gender = "Male"
        else:
            gender = "Female"

        #count total days

        if days >= 500:
            days = days - 500
        else:
            days = days

        #Check month and day (Leap year format)

        if days <= 31:
            month = "January"
            day = days - 0
        elif days <= 60:
            month = "February"
            day = days - 31
        elif days <= 91:
            month = "March"
            day = days - 60
        elif days <= 121:
            month = "April"
            day = days - 91
        elif days <= 152:
            month = "May"
            day = days - 121
        elif days <= 182:
            month = "June"
            day = days - 152
        elif days <= 213:
            month = "July"
            day = days - 182
        elif days <= 244:
            month = "Auguest"
            day = days - 213
        elif days <= 274:
            month = "September"
            day = days - 244
        elif days <= 305:
            month = "Octomber"
            day = days - 274
        elif days <= 335:
            month = "November"
            day = days - 305
        elif days <= 366:
            month = "December"
            day = days - 335
        else:
            message.reply_text("Something Wrong! Please Check Your Identy Card Number...")

        #check year (leap year or not)

        def check_year():
            if year % 4 == 0:
                if year % 100 == 0:
                    if year % 400 == 0:
                        return "Leap year"
                    else:
                        return "Not Leap year"
                else:
                    return "Leap year"
            else:
                return "Not Leap year"
        year_type = check_year()

        #change "days" data type to str

        if day < 10:
            day = "0" + str(day)
        else:
            day = day

        #message.reply_text output

        bot.set_parse_mode()
        message.reply_text(f"""
        NIC Number : {id_number}
Birth Day  : {str(year)} {month} {day}
Gender     : {gender}

Birth Year Type : {year_type}
    
**Now, You can enter other NIC number...**

@NICSriLankaBOT Github repo: <a href="https://github.com/shanelkapramuditha/NIC-Sri-Lanka-BOT">here</a>
""", disable_web_page_preview=True)
        



bot.run()
