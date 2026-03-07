from aiogram import Router, F
from aiogram.types import (Message, 
                           CallbackQuery, 
                           InlineKeyboardMarkup, 
                           InlineKeyboardButton)
from lexicons.lexicon import MAIN_MENU
from aiogram.filters import CommandStart
from keyboards.main_menu import inline_markup, MainMenuCBdata


router: Router = Router(name=__name__)

@router.callback_query(F.data == 'main')
@router.message(CommandStart())
async def main_menu_message(update: Message | CallbackQuery):
    if isinstance(update, Message):
        await update.answer(
            text='Привет, это мой первый начинающий серьезный проект!',
            reply_markup=inline_markup(MAIN_MENU)
            )
    else:
        await update.message.edit_text(
            text='Привет, это мой первый начинающий серьезный проект!',
            reply_markup=inline_markup(MAIN_MENU)
        )
    
@router.callback_query(MainMenuCBdata.filter())
async def callback_menu_action(callback: CallbackQuery, callback_data: MainMenuCBdata):

    menu_desc: dict[str, str] = MAIN_MENU.get(callback_data.menu)

    await callback.message.edit_text(
        text=menu_desc['description'],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", 
                                callback_data="main")]
            ]
        )
    )