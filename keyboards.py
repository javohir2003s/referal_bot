from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Referal havola"),
        KeyboardButton(text="Mening ballarim"),
        KeyboardButton(text="Link olish"),
    ]
    
],
    resize_keyboard=True,
    is_persistent=True
)