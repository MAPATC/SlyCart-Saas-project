from aiogram.filters.callback_data import CallbackData
from aiogram.types import (InlineKeyboardButton, 
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MainMenuCBdata(CallbackData, prefix='menu'):
    menu: str


class TariffCBdata(CallbackData, prefix='tariff'):
    plan: str
    menu: str

def inline_markup(menu: dict) -> InlineKeyboardMarkup:  
    inl_kb_markup = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=menu['text'], callback_data=MainMenuCBdata(menu=menu_cb).pack()) 
               for menu_cb, menu in menu.items()]

    inl_kb_markup.row(*buttons, width=1)

    return inl_kb_markup.as_markup()

def inline_tariffs_markup(tariff: dict, menu: str) -> InlineKeyboardMarkup:
    inl_kb_builder = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=text, callback_data=TariffCBdata(plan=callback_data, menu=menu).pack())
               for callback_data, text in tariff.items()]
    
    buttons.append(InlineKeyboardButton(text="Назад", callback_data="main"))

    inl_kb_builder.row(*buttons, width=1)

    return (inl_kb_builder.as_markup())

if __name__ == "__main__":
    TARIFF: dict[str, str] = {
    "free": "Бесплатный тариф",
    "advanced": "Тариф Бизнес",
    "premium": "Тариф Ультима"
}
 
    print(inline_tariffs_markup(TARIFF, "tariff"))