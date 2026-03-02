from aiogram.types import (InlineKeyboardButton, 
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

def inline_markup(menu: dict) -> InlineKeyboardMarkup:
    inl_kb_markup = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=menu['text'], callback_data=f"menu:{menu_cb}") 
               for menu_cb, menu in menu.items()]

    inl_kb_markup.row(*buttons, width=1)

    return inl_kb_markup.as_markup()