from pyrogram import Client, filters
import datetime
import pytz

#get time now as time_now

time_zone = pytz.timezone('Asia/Colombo')
today = datetime.datetime.now(tz = time_zone)

#get telegram account access

bot = Client("NICSriLankaBot", config_file = "config.ini")

#start command

@bot.on_message(filters.command(commands = ["start"]))
def welcome(client, message):
    bot.set_parse_mode()
    message.reply_text(text = """Hi Welcome...
I'm @NICSriLankaBOT
I can calculate birthday and age with new and old NIC numbers.

@NICSriLankaBOT Github repo: <a href="https://github.com/shanelkapramuditha/NIC-Sri-Lanka-BOT">here</a>

Enter NIC Number...""", disable_web_page_preview=True)

###########calculation part
#get correct id

@bot.on_message(filters.text)
def start(client, message):
    def check_id():
        while True:
            id_number = (message.text).upper()

            #check new nic
            if len(id_number) == 12:
                birth_year = int(id_number[0:4])
                birth_days = int(id_number[4:7])
                if (datetime.date(birth_year + 1, 1, 1) - datetime.date(birth_year, 1,1) == datetime.timedelta(days=366)):
                    if (0 < birth_days <= 366 or 0 < birth_days - 500 <= 366) and today.year - birth_year >= 16 and birth_year > 1900:
                        return id_number, birth_year, birth_days, "Leap year"
                    else:
                        message.reply_text("Please check your NIC number and Enter again...")
                        return "wrong"
                elif datetime.date(birth_year + 1, 1, 1) - datetime.date(birth_year, 1,1) == datetime.timedelta(days=365):
                    if (0 < birth_days <= 365 or 0 < birth_days - 500 <= 365) and today.year - birth_year >= 16 and birth_year > 1900:
                        return id_number, birth_year, birth_days, "Not Leap year"
                    else:
                        message.reply_text("Please check your NIC number and Enter again...")
                        return "wrong"

            #check old nic
            elif len(id_number) == 10:
                birth_year = int("19"+str(id_number[0:2]))
                birth_days = int(id_number[2:5])
                
                if "V" in id_number[9] and datetime.date(birth_year + 1, 1, 1) - datetime.date(birth_year, 1,1) == datetime.timedelta(days=366):
                    if (0 < birth_days <= 366 or 0 < birth_days - 500 <= 366) and today.year - birth_year >= 16 and birth_year > 1900:
                        return id_number, birth_year, birth_days, "Leap year"
                    else:
                        message.reply_text("Please check your NIC number and Enter again...")
                        return "wrong"
                elif "V" in id_number[9] and (datetime.date(birth_year + 1, 1, 1) - datetime.date(birth_year, 1,1) == datetime.timedelta(days=365)):
                    if (0 < birth_days <= 365 or 0 < birth_days - 500 <= 365) and today.year - birth_year >= 16 and birth_year > 1900:
                        return id_number, birth_year, birth_days, "Not Leap year"
                    else:
                        message.reply_text("Please check your NIC number and Enter again...")
                        return "wrong"
            
            #wrong nic
            else:
                message.reply_text("Please check your NIC number and Enter again...")
                return "wrong"

    id_info = check_id()

    if id_info != "wrong":
        id_number = id_info[0]
        birth_year = id_info[1]
        birth_days = id_info[2]
        year_type = id_info[3]
    
        #check gender and count days

        if birth_days < 500:
            gender = "Male"
        else:
            gender = "Female"
            birth_days = birth_days - 500

        #calculate birth day

        birth_day = datetime.timedelta(birth_days - 1) + datetime.datetime(birth_year, 1, 1)

        #skip feb 29

        if year_type == "Not Leap year" and birth_day.month > 2:
            birth_day = datetime.timedelta(birth_days - 2) + datetime.datetime(birth_year, 1, 1)

        #calculate age in days

        today_str = str(today)[:10].split('-')
        lived_days = datetime.datetime(int(today_str[0]), int(today_str[1]), int(today_str[2])) - birth_day
        lived_days = str(lived_days).split(', ')[0]

        # age in year, month, days
        if today.month >= birth_day.month:
            age_year = str(today.year - birth_day.year) + " years"
            if today.day >= birth_day.day:
                age_month = str(today.month - birth_day.month) + " months"
                age_days = str(today.day - birth_day.day) + " days"
            else:
                age_month = str(today.month - birth_day.month - 1) + " months"
                age_month_int = today.month - birth_day.month - 1
                age_days = str(datetime.datetime(today.year, today.month, today.day) - datetime.datetime(today.year, birth_day.month + age_month_int, birth_day.day)).split(", ")[0]

        else:
            age_year = str(today.year - birth_day.year - 1) + " years"

        age = f"{age_year} {age_month} {age_days}"

        #message.reply_text output

        bot.set_parse_mode()
        message.reply_text(f"""
        ```NIC Number : {id_number}

Birth Day : {birth_day.strftime('%Y %B %d')}

Gender : {gender}

Age : {age}

Number of days lived : {lived_days}

Birth Year Type : {year_type}


Checked Date : {today.strftime('%Y/%m/%d')}```


@NICSriLankaBOT Github repo: <a href="https://github.com/shanelkapramuditha/NIC-Sri-Lanka-BOT">here</a>

**Now, You can enter other NIC number...**
""", disable_web_page_preview=True)
        
bot.run()
