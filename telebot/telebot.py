from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import datetime
import aioschedule
import os
from pathlib import Path
from data import  get_schedule,chat_id_load,chat_id_save

bot = Bot(token="8356760620:AAEFaQ_p-ebnCzOyDBZVVj0zWwU6UH92Jr0")
dp = Dispatcher()



teacher = "Цымлов Алексей Васильевич"
send_time = "21:00"
delta_days = 0



chat_id = chat_id_load()

@dp.message(Command("start"))
async def start(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    
    chat_id_save(chat_id)
    

    print(f"🆔 Новый старт: Chat ID={chat_id}, User ID={message.from_user.id}")
    await message.answer("✅ Чат зарегистрирован для получения уведомлений!")

async def send_notification():

    date = (datetime.date.today() + datetime.timedelta(days=delta_days)).strftime("%d.%m.%Y")
    schedule_data = get_schedule(teacher, date)
    
    if not schedule_data or chat_id is None:
        return

    groups = set()
    for pair in schedule_data:
        for group in schedule_data[pair]:
            if group:
                groups.add(group)
    

    groups_list = ", ".join(sorted(groups))
    message = f"📅 Расписание на {date}:\n"
    message += f"У групп {groups_list} завтра занятие. Не опаздывать!"
    


    
    try:
        await bot.send_message(
            chat_id=chat_id, 
            text=message
        )
    except Exception as e:
        print(f"❌ Ошибка отправки в чат {chat_id}: {e}")


async def send_message_by_shedule():
    aioschedule.every().day.at(send_time).do(send_notification)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)

async def main():
    print("🧪 Тестовая отправка...")
    await send_message_by_shedule()
    await send_notification()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")