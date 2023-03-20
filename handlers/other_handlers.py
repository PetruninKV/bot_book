from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON
import random

router: Router = Router()


@router.message()
async def other_messages(messages: Message):
    text = random.choice(LEXICON['other_messages'])
    await messages.answer(text=text)