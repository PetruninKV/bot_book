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
    

@router.message(Command(commands='continue'))
async def continue_message(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(text=text,
                         reply_markup=create_pagination_keyboard( 
                                                    'backward',
                                                    f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                                                    'forward'))
    

@router.message(Command(commands='bookmarks'))
async def bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON['/bookmarks'],
            reply_markup=create_bookmarks_keyboard(*users_db[message.from_user.id]['bookmarks']))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(Text(text='forward'))
async def forward_callback(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,
                                        reply_markup=create_pagination_keyboard( 
                                                    'backward',
                                                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                                                    'forward'))
    await callback.answer()


@router.callback_query(Text(text='backward'))
async def backward_callback(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,
                                         reply_markup=create_pagination_keyboard( 
                                                    'backward',
                                                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                                                    'forward'))
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def page_callback(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(users_db[callback.from_user.id]['page'])
    await callback.answer(text='Страница добавлена в закладки')


@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
                text=LEXICON[callback.data],
                reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()
        

