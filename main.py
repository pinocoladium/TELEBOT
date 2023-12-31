import asyncio
import logging
import os
import shutil
import sys
import time

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

from db.models import Base, Session, Wish_list, conn, engine
from functions.get_photo_func import get_photo, get_user_photo
from functions.reportlab_func import wish_list_func

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)


class Form(StatesGroup):
    wish_list = State()
    processing_wish_list = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [
        [types.KeyboardButton(text="Ну что ж, начнём")],
        [types.KeyboardButton(text="Не, спасибо")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери ответ из предложенного",
        one_time_keyboard=True,
    )
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker="CAACAgIAAxkBAAEK1KVlZKfWFT29zSEszVwZxvn0c5crTAACvhcAAlC3CUt0MEIgcVRNdDME",
    )
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}, я бот, который поможет тебе, ленивому созданию, составить так называемый wish list, что в переводе с английского означает список желаний"
    )
    await message.answer("Ну что же, приступим к делу?", reply_markup=keyboard)


@dp.message(F.text.lower() == "не, спасибо")
async def do_wishlist(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Ну что ж, начнём")],
        [types.KeyboardButton(text="Не, спасибо")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери ответ из предложенного",
        one_time_keyboard=True,
    )
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker="CAACAgIAAxkBAAEK1J9lZKa3Cy4KFPyAPSUUQ0OEfiNpTgACKQADbmmPFYmoZGvc0bEiMwQ",
    )
    await message.reply(
        "Ответ неправильный!!! Подумайте ещё, и на этот раз реализуйте все свои интеллектуальные возможности"
    )
    await message.answer("Ну что же, приступим к делу?", reply_markup=keyboard)


@dp.message(Command("instruction"))
@dp.message(F.text.lower() == "ну что ж, начнём")
async def instructions_first(message: types.Message):
    await message.answer("Сейчас я объясню, как мы будем всё это делать")
    await message.answer(
        "Что тебе нужно сейчас сделать:\n1. Отправить мне скриншот/фото желаемого подарка и сразу же написать к нему описание\n2. После описания поставить тире (-) и дальше отправить ссылку на подарок\n3. Если ты не хочешь вставлять ссылку, после тире (-) пиши «нет»\n\n\nПример  ⬇️"
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile("static/primer/primer.png"),
        caption="Готов принять такое в дар, и не забудьте поставить фсошки - https://ozon.ru/t/BK5GKo4",
    )
    await message.answer("После отправки обязательно дождись моего сообщения!")
    await message.answer(
        "Как только ты закончишь создание своего вишлиста, нажми на КНОПКУ, она будет всплывать после каждого моего ответного сообщения"
    )
    kb = [
        [types.KeyboardButton(text="Да, все ясно")],
        [types.KeyboardButton(text="Ничего не понятно")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери ответ из предложенного",
        one_time_keyboard=True,
    )
    await message.answer("Все понятно?", reply_markup=keyboard)


@dp.message(F.text.lower() == "ничего не понятно")
async def instructions_second(message: types.Message):
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker="CAACAgIAAxkBAAEK1J1lZKaG24jAHMeqTq9fPudQuoXWkQAC9Z4AAmOLRgx36jy0bqgKZTME",
    )
    await message.answer("Хорошо, давай ещё раз")
    await message.answer(
        "Что тебе нужно сейчас сделать:\n1. Отправить мне скриншот/фото желаемого подарка и сразу же написать к нему описание\n2. После описания поставить тире (-) и дальше отправить ссылку на подарок\n3. Если ты не хочешь вставлять ссылку, после тире (-) пиши «нет»\n\n\nПример  ⬇️"
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile("static/primer/primer.png"),
        caption="Готов принять такое в дар, и не забудьте поставить фсошки - https://ozon.ru/t/BK5GKo4",
    )
    await message.answer("После отправки обязательно дождись моего сообщения!")
    await message.answer(
        "Как только ты закончишь создание своего вишлиста, нажми на КНОПКУ, она будет всплывать после каждого моего ответного сообщения"
    )
    kb = [
        [types.KeyboardButton(text="Да, все ясно")],
        [types.KeyboardButton(text="Ничего не понятно")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери ответ из предложенного",
        one_time_keyboard=True,
    )
    await message.answer("А теперь всё понятно?", reply_markup=keyboard)


@dp.message(Command("wishlist"))
@dp.message(F.text.lower() == "да, все ясно")
async def wish_list(message: types.Message, state: FSMContext):
    await state.set_state(Form.wish_list)
    await message.answer("Хорошо, приступим, кидай скриншот с описанием")


@dp.message(Form.wish_list)
async def wish_list(message: Message, state: FSMContext):
    dir_name = f"static/image/{message.from_user.full_name}"
    img_name = time.time()
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if not message.photo:
        await message.answer("Не вижу твоего фото")
        await message.answer("Давай еще раз повторим")
        await message.answer("Кидай фото с описанием")
        return
    image_path = await get_photo(bot, message.photo[-1].file_id, dir_name, img_name)
    description = message.caption.split("-")[0]
    link = message.caption.split("-")[1].replace(" ", "")
    new_wish_list = Wish_list(
        full_name=message.from_user.full_name,
        image_path=image_path,
        description=description,
        link=link,
    )
    try:
        with Session() as session:
            session.add(new_wish_list)
            session.commit()
    except IntegrityError as err:
        await message.answer("Произошла неизвестная ошибка, ой-ой...")
        await message.answer("Посмотри, правильно ли ты составил сообщение")
        await message.answer("Попробуй еще раз скинуть")
        await bot.send_message(
            chat_id=os.getenv("SUP_CHAT"),
            text=f"Произошла ошибка с пользователем {message.from_user.full_name} - {err}",
        )
    else:
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="⚠ TА САМАЯ КНОПКА ⚠", callback_data="finish"
            )
        )
        await message.answer("Принял, кидай дальше", reply_markup=builder.as_markup())


@dp.callback_query(F.data == "finish")
async def trans_wish_list(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.processing_wish_list)
    await callback.message.answer("Понял, переходим на другую стадию")
    kb = [
        [types.KeyboardButton(text="Да, всё хорошо")],
        [types.KeyboardButton(text="Нет, мне не понравилось")],
        [types.KeyboardButton(text="Не знаю, что написать")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери ответ из предложенного",
        one_time_keyboard=True,
    )
    await callback.message.answer(
        "Как прошел процесс? Всё ли было просто? Можешь оставить свой развернутый отзыв или пожелание, либо просто выбрать из предложенного ниже",
        reply_markup=keyboard,
    )
    await callback.answer()


@dp.message(Form.processing_wish_list)
async def wish_list(message: Message, state: FSMContext):
    await state.clear()
    await bot.send_message(
        chat_id=os.getenv("SUP_CHAT"),
        text=f"Пользователь {message.from_user.full_name} оставил такую заметку - {message.text}",
    )
    await message.answer(
        "Отлично, тогда сейчас я попробую обработать твои пожелания..."
    )
    with conn.cursor() as curs:
        curs.execute(
            f"SELECT full_name, image_path, description, link FROM wish_list_table WHERE full_name = %s",
            (message.from_user.full_name,),
        )
        wish_list = curs.fetchall()
    if not wish_list:
        await message.answer("Твоих данных в таблице уже нет, начинай все заново")
        await state.set_state(Form.wish_list)
        await message.answer("Кидай фото с описанием")
        return
    file_path = wish_list_func(
        wish_list,
        await get_user_photo(
            bot, message.from_user.id, f"static/image/{message.from_user.full_name}"
        ),
    )
    await message.answer("Готово, осталось загрузить...")
    await bot.send_document(chat_id=message.chat.id, document=FSInputFile(file_path))
    await message.answer("Вуаля, это твой вишлист, отправь его своим друзьям")
    await message.answer("И это было вовсе не легко")
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker="CAACAgIAAxkBAAEK1KFlZKd1gaAW2r9MZRFBMlKGkHXOhwACzRsAApY7uhf4_XGfImUGijME",
    )
    await message.answer("Если захочешь составить еще один вишлист, жми /wishlist")
    with conn.cursor() as curs:
        curs.execute(
            f"DELETE FROM wish_list_table WHERE full_name = %s",
            (message.from_user.full_name,),
        )
        dir_name = f"static/image/{message.from_user.full_name}"
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    if os.path.isfile(file_path):
        os.remove(file_path)


@dp.message()
@dp.message(Command("help"))
async def echo_handler(message: types.Message) -> None:
    await message.reply(
        "Я же не ChatGPT, реагировать на подобное внесюжетное обращение еще не умею ..."
    )
    await message.answer(
        "/instruction - жми, чтобы увидеть инструкцию о том, как необходимо взаимодействовать с ботом для составления вишлиста\n /wishlist - жми, чтобы начать взаимодействие с ботом для составления вишлиста"
    )


async def main() -> None:
    await dp.start_polling(bot)


async def init_models():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(init_models())
    asyncio.run(main())
