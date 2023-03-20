from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import (create_bookmarks_keyboard, create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book


router: Router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=LEXICON['/start'])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands='beginning'))
async def beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(text=text, 
                         reply_markup=create_pagination_keyboard( 
                                                    'backward',
                                                    f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                                                    'forward'))
    
