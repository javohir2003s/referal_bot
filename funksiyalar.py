from aiogram.types import Message
from aiogram import Bot, types, F
from aiogram.fsm.context import FSMContext
from sqlite_db import DataBase
from environs import Env
from loader import dp

from keyboards import main_menu

db_objects = DataBase("db.sqlite3")

CHANNEL_ID = "-1002146591414"

async def start_command(message: Message, bot: Bot):
    if message.text[7:].isdigit():
        if db_objects.get_user(message.from_user.id):
            
            if message.text[7:] == message.from_user.id:
                await message.answer("Siz o'zingizga referal bo'la olmaysiz")
                
            else:
                await message.answer("Siz oldin botga tashrif buyurgansiz va referal bo'la olmaysiz")
        
        else:
            refer_id = message.text[7:]
            db_objects.add_user(user_id=message.from_user.id, refer_id=refer_id, full_name=message.from_user.full_name, flag='False')

            inline=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text="Qani kanalga a'zo bo'lingchi 🤨", url="https://t.me/+4WF1dAwDBS5jYzc6")],
                    [types.InlineKeyboardButton(text="A'zo bo'ldim 🙃", callback_data="azo")]
                ],
                row_width=2
            )
                
            await message.answer("Kanalga a'zo bo'ling xay 😏", reply_markup=inline)

    else:       
        if db_objects.get_user(message.from_user.id) and db_objects.get_user(message.from_user.id)[4] == "True":
            await message.answer("Asosiy menudasiz!", reply_markup=main_menu)
            
            # if db_objects.get_user_ball(message.from_user.id)[0] >=6:
            res = db_objects.get_user_ball(message.from_user.id)
        
        elif db_objects.get_user(message.from_user.id):
            user_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
            
            if user_status.status in ['member', 'administrator', 'creator']:
                db_objects.update_user(user_id=message.from_user.id)
                await message.answer('Botdan foydalanish mumkin',  reply_markup=main_menu)
                
            else:
                inline=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [types.InlineKeyboardButton(text="Qani kanalga a'zo bo'lingchi 🤨", url="https://t.me/+4WF1dAwDBS5jYzc6")],
                        [types.InlineKeyboardButton(text="A'zo bo'ldim 🙃", callback_data="azo")]
                    ],
                    row_width=2
                )
                
                await message.answer("Hoy bo'tam kanalga kim a'zo bo'ladi 😏", reply_markup=inline)

        else:
            db_objects.add_user(user_id=message.from_user.id, refer_id=None, full_name=message.from_user.full_name, flag='False')
            
            inline=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [types.InlineKeyboardButton(text="Qani kanalga a'zo bo'lingchi 🤨", url="https://t.me/+4WF1dAwDBS5jYzc6")],
                        [types.InlineKeyboardButton(text="A'zo bo'ldim 🙃", callback_data="azo")]
                    ],
                    row_width=2
                )
                
            await message.answer("Kanalga a'zo bo'ling xay 😏", reply_markup=inline)
            
       
@dp.callback_query(F.data == "azo")    
async def calback(callback: types.CallbackQuery, bot: Bot):
    user_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback.from_user.id)
    
    if user_status.status in ['member', 'administrator', 'creator']:
        db_objects.update_user(user_id=callback.from_user.id)
        await callback.answer('Botdan foydalanish mumkin',  reply_markup=main_menu)
        
    else:
        inline=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Qani kanalga a'zo bo'lingchi 🤨", url="https://t.me/+4WF1dAwDBS5jYzc6")],
                [types.InlineKeyboardButton(text="A'zo bo'ldim 🙃", callback_data="azo")]
            ],
            row_width=2
        )
        
        await callback.answer("Hoy bo'tam kanalga kim a'zo bo'ladi 😏", reply_markup=inline)    
        
        

async def get_ref_link_answer(message: Message):
    if db_objects.get_user(message.from_user.id):
        ref_link = f"https://t.me/RamazondaYuksalamiz_bot?start={message.from_user.id}"
    
        await message.answer(f"Sizning referal havolangiz: \n\n {ref_link}")
    
    else:
        inline=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Qani kanalga a'zo bo'lingchi 🤨", url="https://t.me/+4WF1dAwDBS5jYzc6")],
                [types.InlineKeyboardButton(text="A'zo bo'ldim 🙃", callback_data="azo")]
            ],
            row_width=2
        )
        
        await message.answer("Hoy bo'tam kanalga kim a'zo bo'ladi 😏", reply_markup=inline)    
        
        
         

async def get_user_ball_answer(message: Message):
    if db_objects.get_user(message.from_user.id):
        user_ball = db_objects.get_user_ball(message.from_user.id)
        
        await message.answer(f"Sizning balingiz \n\n {user_ball} ball")

    else:
        await message.answer("Botga start bosmagansiz")
        


async def get_special_link(message: Message):
    if db_objects.get_user(message.from_user.id) and db_objects.get_user_ball(message.from_user.id)>=5:
        await message.answer(f"Siz hamma shartni bajardiz sizda 5 tandan ortiq referal bor")
        
    if db_objects.get_user(message.from_user.id) and db_objects.get_user_ball(message.from_user.id)<5:
        await message.answer(f"Sizda yetarli referal yo'q")

    if db_objects.get_user(message.from_user.id) == 0:
        await message.answer("Botga start bosmagansiz")