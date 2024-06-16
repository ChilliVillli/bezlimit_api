from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Тариф'),
            KeyboardButton(text='Маска'),
            KeyboardButton(text='Категория')
        ]
    ],
    resize_keyboard=True
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выберите тариф')
        ]
    ],
    resize_keyboard=True
)


tarif_num = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='590'),
            KeyboardButton(text='790'),
            KeyboardButton(text='1000')
        ],
        [
            KeyboardButton(text='1250'),
            KeyboardButton(text='1500'),
            KeyboardButton(text='2000')
        ],
        [
            KeyboardButton(text='2500'),
            KeyboardButton(text='3000'),
            KeyboardButton(text='4000')
        ],
        [
            KeyboardButton(text='Пропустить')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


cat = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='bronze'),
            KeyboardButton(text='silver'),
            KeyboardButton(text='gold')
        ],
        [
            KeyboardButton(text='platinum'),
            KeyboardButton(text='brilliant')
        ],
        [
            KeyboardButton(text='Пропустить')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

next = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пропустить')
        ]
    ],
    resize_keyboard=True
)


cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='отмена поиска')
        ]
    ],
    resize_keyboard=True
)