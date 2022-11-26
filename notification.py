from loader import bot, db
from datetime import datetime
from datetime import timedelta
import asyncio


async def notify():
    
    result= db.get_info()
    for i in result:
        id= i[0]

        td= datetime.today()
        user_dt= datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S') - timedelta(hours=i[2]) + timedelta(minutes=i[4])
        if td.hour == user_dt.hour and td.minute == user_dt.minute:
            if i[3] == None:
                if i[4] == 0:
                    for j in range(0,5):
                        await bot.send_message(chat_id=str(id), text="Просыпайся, опоздаешь")
                        await asyncio.sleep(1)
                else:
                    await bot.send_message(chat_id=str(id), text="Просыпайся, опоздаешь")
                if i[4] == 15:
                    db.delete(user_id=id, dt=i[1])
                else:
                    db.alarm(id)
            else:
                await bot.send_message(chat_id=str(id), text=i[3]) 
                db.delete(user_id=id, dt=i[1])
        