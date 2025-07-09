from aiogram import F, Bot
from aiogram.filters import CommandStart, Command  
import funksiyalar
from asyncio import run
from environs import Env
from loader import dp
from aiogram.types import BotCommand
env = Env()
env.read_env()


ADMINS = int(env("ADMINS"))


async def startup_answer(bot: Bot):
    await bot.send_message(chat_id=ADMINS, text="Bot ishga tushdi")
    
async def shutdown_answer(bot: Bot):
    await bot.send_message(chat_id=ADMINS, text="Bot to'xtadi")
    

async def start():
    dp.startup.register(startup_answer)
    dp.shutdown.register(shutdown_answer)
    
    dp.message.register(funksiyalar.start_command, CommandStart())
    dp.message.register(funksiyalar.admins_command, Command('admins'))
    dp.message.register(funksiyalar.get_ref_link_answer, F.text== "Referal havola")
    dp.message.register(funksiyalar.get_user_ball_answer, F.text=="Mening ballarim")
    dp.message.register(funksiyalar. get_special_link, F.text=="Link olish")
    dp.message.register(funksiyalar.get_users_list, F.text == "A'zolar")
    
    bot = Bot(token=env("BOT_TOKEN"))
    
    await bot.set_my_commands([
        BotCommand(command='/start', description="Botni ishga tushirish"),
        BotCommand(command="/admins", description="Adminlar uchun")
    ])
    
    await dp.start_polling(bot, polling_timeout=1)
    
run(start())