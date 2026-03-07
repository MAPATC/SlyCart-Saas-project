from aiogram.filters.callback_data import CallbackData
from aiogram.types import (InlineKeyboardButton, 
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MainMenuCBdata(CallbackData, prefix='menu'):
    menu: str

def inline_markup(menu: dict) -> InlineKeyboardMarkup:  
    inl_kb_markup = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=menu['text'], callback_data=MainMenuCBdata(menu=menu_cb).pack()) 
               for menu_cb, menu in menu.items()]

    inl_kb_markup.row(*buttons, width=1)

    return inl_kb_markup.as_markup()