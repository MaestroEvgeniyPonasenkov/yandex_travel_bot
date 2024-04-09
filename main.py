import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher()

# <a href="{config.group_link}">вступить</a>
# {config.promo}
# <a href="https://t.me/yandex_travel_chats/3">Поделитесь</a>


def last_day_of_month():
    today = datetime.now()
    first_day_of_next_month = (today.replace(
        day=1) + timedelta(days=32)).replace(day=1)
    last_day_of_month = first_day_of_next_month - timedelta(days=1)
    months = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря"
    }
    month_name = months[last_day_of_month.month]
    formatted_date = f"{last_day_of_month.day} {month_name} {last_day_of_month.year} года"
    return formatted_date

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    chat_member = await bot.get_chat_member(config.group_id, message.from_user.id)
    if chat_member.status not in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Я подписался", callback_data="sub"))
        await message.answer(
            f'''
Привет! Рады видеть вас в клубе Яндекс Путешественников. Чтобы получить промокод, нужно <a href="{config.group_link}">вступить</a> в наш чат. ''', parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
    else:
        await message.answer(f'''
Ура, промокод на скидку до 20% уже здесь: {config.promo}

Максимальная скидка: 2000 ₽. Действует на один заказ на бронирование отеля в <a href="https://redirect.appmetrica.yandex.com/serve/1181039353179218124?afpub_id=smm&site_id=telegram&creative_id=chat03">мобильном приложении</a> Яндекс Путешествий до {last_day_of_month()}. <a href="https://yandex.ru/legal/travel_promocode/">Условия</a> использования промокода.

Куда планируете поехать в отпуск? <a href="https://t.me/yandex_travel_chats/3">Поделитесь</a> идеями с другими путешественниками🌍''', parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@dp.callback_query(F.data == "sub")
async def send_promo(callback: types.CallbackQuery):
    chat_member = await bot.get_chat_member(config.group_id, callback.from_user.id)
    if chat_member.status not in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        await callback.answer(text="Вы не подписаны!", show_alert=True)
    else:
        await callback.message.answer(f'''
Ура, промокод на скидку до 20% уже здесь: {config.promo}

Максимальная скидка: 2000 ₽. Действует на один заказ на бронирование отеля в <a href="https://redirect.appmetrica.yandex.com/serve/1181039353179218124?afpub_id=smm&site_id=telegram&creative_id=chat03">мобильном приложении</a> Яндекс Путешествий до {last_day_of_month()}. <a href="https://yandex.ru/legal/travel_promocode/">Условия</a> использования промокода.

Куда планируете поехать в отпуск? <a href="https://t.me/yandex_travel_chats/3">Поделитесь</a> идеями с другими путешественниками🌍''', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        await callback.answer()


@dp.message(F.text)
async def all_messages(message: types.Message):
    await message.answer('Отправьте боту /start, чтобы начать работу!')


# @dp.message(F.content_type == types.ContentType.NEW_CHAT_MEMBERS)
# async def new_chat_members(message: types.Message):
#     new_members = message.new_chat_members
#     for member in new_members:
#         await message.answer(f"Добро пожаловать, {member.first_name}!")
#         print(message.chat.id)
#         await bot.send_message(chat_id=member.id, text='Привет)')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
