from lexicons.lexicon import MAIN_MENU
from aiogram.types import (InlineKeyboardButton, 
                           InlineKeyboardMarkup, 
                           Message,
                           CallbackQuery)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart

router: Router = Router(name=__name__)

def inline_markup() -> InlineKeyboardMarkup:
    inl_kb_markup =InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=menu['text'], callback_data=menu_cb) 
               for menu_cb, menu in MAIN_MENU.items()]

    inl_kb_markup.row(*buttons, width=1)

    return inl_kb_markup.as_markup()