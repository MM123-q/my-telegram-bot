import os
from aiohttp import web
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery,
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardRemove
)

# Настройка логирования в консоли
logging.basicConfig(level=logging.INFO)

# =====================================================================
# ⚠️ НАСТРОЙКИ БОТА (ВСТАВЬ СВОИ ДАННЫЕ НИЖЕ)
# =====================================================================

BOT_TOKEN = "8958700814:AAFtAfc2Ms8Irn1-EHycgEmAryTIt_CeGoc"

# Укажи здесь свой личный Telegram ID (узнать у @userinfobot) 
# или отрицательный ID вашей общей группы сотрудников (например, -100123456789)
GROUP_CHAT_ID = -5223351329

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Ссылка на рекламный баннер
BANNER_URL = "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1000"


# =====================================================================
# СОСТОЯНИЯ FSM (МАШИНА СОСТОЯНИЙ ДЛЯ СБОРА ЗАЯВКИ)
# =====================================================================

class OrderForm(StatesGroup):
    waiting_for_service = State()  # Шаг 1: Описание задачи/услуги
    waiting_for_name = State()     # Шаг 2: Имя клиента
    waiting_for_phone = State()    # Шаг 3: Номер телефона


# =====================================================================
# КЛАВИАТУРЫ (КНОПКИ)
# =====================================================================

# 1. Сетка кнопок Главного меню
def get_main_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📝 Оставить заявку на расчет", callback_data="start_order")
        ],
        [
            InlineKeyboardButton(text="🍕 Каталог товаров", callback_data="open_catalog"),
            InlineKeyboardButton(text="💰 Прайс & Цены", callback_data="open_price")
        ],
        [
            InlineKeyboardButton(text="🏢 О компании", callback_data="open_about"),
            InlineKeyboardButton(text="⭐ Отзывы", callback_data="open_reviews")
        ],
        [
            InlineKeyboardButton(text="📞 Связаться с менеджером", callback_data="open_contacts")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# 2. Кнопка возврата в главное меню
def get_back_keyboard():
    buttons = [
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# =====================================================================
# ОБРАБОТЧИКИ (HANDLERS) — КОМАНДЫ И КНОПКИ МЕНЮ
# =====================================================================

# Команда /start — Запуск бота
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    
    caption_text = (
        f"👋 <b>Приветствуем вас в Almaty Dev Studio!</b>\n\n"
        f"Мы разрабатываем быстрых и удобных Telegram-ботов для бизнеса в Алматы. "
        f"Автоматизируем продажи, прием заявок и запись клиентов 24/7.\n\n"
        f"🔥 <b>Почему выбирают нас:</b>\n"
        f"• Более 30+ успешных проектов\n"
        f"• Разработка под ключ от 3 дней\n"
        f"• Гарантия и техподдержка 1 год\n\n"
        f"👇 <b>Выберите интересующий раздел ниже:</b>"
    )
    
    await message.answer_photo(
        photo=BANNER_URL,
        caption=caption_text,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )


# 1️⃣ Раздел «Каталог»
@dp.callback_query(F.data == "open_catalog")
async def show_catalog(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=(
            "🍕 <b>Каталог готовых решений:</b>\n\n"
            "1. <b>Бот-магазин</b> с корзиной и Kaspi Pay — от 80 000 ₸\n"
            "2. <b>Бот записи</b> для салонов/клиник — от 50 000 ₸\n"
            "3. <b>Бот для курсов</b> (Защита материалов) — от 60 000 ₸"
        ),
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# 2️⃣ Раздел «Прайс & Цены»
@dp.callback_query(F.data == "open_price")
async def show_price(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=(
            "💰 <b>Наш прайс-лист на услуги:</b>\n\n"
            "• <b>Простой бот-визитка:</b> от 40 000 ₸\n"
            "• <b>Бот с записью / календарем:</b> от 65 000 ₸\n"
            "• <b>Интернет-магазин в Telegram:</b> от 100 000 ₸\n"
            "• <b>Интеграция с CRM / Каспи:</b> от 30 000 ₸\n\n"
            "⏱ <i>Сроки разработки — от 3 до 7 рабочих дней.</i>"
        ),
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# 3️⃣ Раздел «О компании»
@dp.callback_query(F.data == "open_about")
async def show_about(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=(
            "🏢 <b>О нашей компании:</b>\n\n"
            "Мы команда IT-разработчиков из Алматы. Создаем ботов, которые увеличивают конверсию продаж и освобождают время предпринимателя.\n\n"
            "📍 Офис: г. Алматы, пр. Абая 150\n"
            "⏱ График работы: Пн-Сб с 9:00 до 20:00"
        ),
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# 4️⃣ Раздел «Отзывы»
@dp.callback_query(F.data == "open_reviews")
async def show_reviews(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=(
            "⭐ <b>Отзывы наших клиентов:</b>\n\n"
            "💬 <i>«Заказывали бота для доставки еды. Заказы стали приходить в 2 раза быстрее!»</i> — Сеть кафе\n\n"
            "💬 <i>«Настроили бота для обучающего центра. Освободили менеджера от рутины.»</i> — Education Club"
        ),
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# 5️⃣ Раздел «Связаться с менеджером»
@dp.callback_query(F.data == "open_contacts")
async def show_contacts(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=(
            "📞 <b>Связь с менеджером:</b>\n\n"
            "Готовы обсудить ваш проект или рассчитать точную стоимость?\n\n"
            "💬 <b>WhatsApp:</b> +7 (700) 000-00-00\n"
            "✈️ <b>Telegram:</b> @manager_almaty\n"
            "📧 <b>Email:</b> info@almatydev.kz\n\n"
            "Отвечаем в течение 5–10 минут в рабочее время!"
        ),
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# 🔄 Кнопка «Назад в главное меню»
@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    caption_text = (
        f"👋 <b>Приветствуем вас в Almaty Dev Studio!</b>\n\n"
        f"Мы разрабатываем быстрых и удобных Telegram-ботов для бизнеса в Алматы. "
        f"Автоматизируем продажи, прием заявок и запись клиентов 24/7.\n\n"
        f"🔥 <b>Почему выбирают нас:</b>\n"
        f"• Более 30+ успешных проектов\n"
        f"• Разработка под ключ от 3 дней\n"
        f"• Гарантия и техподдержка 1 год\n\n"
        f"👇 <b>Выберите интересующий раздел ниже:</b>"
    )
    await callback.message.edit_caption(
        caption=caption_text,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# =====================================================================
# ОБРАБОТЧИКИ FSM — ПОШАГОВЫЙ СБОР ЗАЯВКИ И ОТПРАВКА В ЧАТ
# =====================================================================

# Шаг 1: Старт сбора заявки
@dp.callback_query(F.data == "start_order")
async def start_order_process(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderForm.waiting_for_service)
    
    await callback.message.answer(
        "📝 <b>Какая услуга или бот вас интересует?</b>\n\n"
        "Напишите кратко, какой проект вы хотите реализовать (например: <i>«Бот для записи в салон»</i> или <i>«Каталог с доставкой»</i>):",
        parse_mode="HTML"
    )
    await callback.answer()


# Шаг 2: Получаем описание задачи и просим Имя
@dp.message(OrderForm.waiting_for_service)
async def process_service(message: types.Message, state: FSMContext):
    await state.update_data(chosen_service=message.text)
    await state.set_state(OrderForm.waiting_for_name)
    
    await message.answer(
        "👍 Отлично!\n\n<b>Как к вам обращаться?</b> Напишите ваше имя:",
        parse_mode="HTML"
    )


# Шаг 3: Получаем Имя и просим Телефон (выводим кнопку отправки контакта)
@dp.message(OrderForm.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await state.set_state(OrderForm.waiting_for_phone)
    
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Поделиться номером телефона", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        f"Приятно познакомиться, <b>{message.text}</b>!\n\n"
        "Остался последний шаг. Нажмите кнопку ниже, чтобы передать номер телефона, или введите его вручную:",
        reply_markup=phone_keyboard,
        parse_mode="HTML"
    )


# Шаг 4: Получаем Телефон, добавляем кнопку "Взять в работу" и отправляем в группу
@dp.message(OrderForm.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    if message.contact:
        user_phone = message.contact.phone_number
    else:
        user_phone = message.text

    user_data = await state.get_data()
    chosen_service = user_data.get("chosen_service", "Не указано")
    user_name = user_data.get("user_name", "Не указано")
    
    username_str = f"@{message.from_user.username}" if message.from_user and message.from_user.username else "Не указан"

    order_card = (
        "🚨 <b>НОВАЯ ЗАЯВКА С БОТА!</b>\n\n"
        f"👤 <b>Клиент:</b> {user_name}\n"
        f"📞 <b>Телефон:</b> {user_phone}\n"
        f"💬 <b>Запрос:</b> {chosen_service}\n\n"
        f"✈️ <b>Telegram профиль:</b> {username_str}\n"
        f"🆔 <b>User ID:</b> <code>{message.from_user.id}</code>"
    )

    # Inline-кнопка для сотрудников в чате
    claim_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔘 Взять в работу", 
                    callback_data=f"claim_{message.from_user.id}"
                )
            ]
        ]
    )
    
    try:
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=order_card,
            reply_markup=claim_keyboard,
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Не удалось отправить заявку в группу: {e}")

    await message.answer(
        "✅ <b>Ваша заявка успешно принята!</b>\n\n"
        "Наш менеджер уже получил уведомление и свяжется с вами в течение 10–15 минут.",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    
    await state.clear()


# =====================================================================
# ОБРАБОТЧИК ДЛЯ МЕНЕДЖЕРОВ: КНОПКА "ВЗЯТЬ В РАБОТУ" В ГРУППЕ
# =====================================================================

@dp.callback_query(F.data.startswith("claim_"))
async def claim_order_handler(callback: CallbackQuery):
    client_id = int(callback.data.split("_")[1])

    manager_username = f"@{callback.from_user.username}" if callback.from_user and callback.from_user.username else callback.from_user.full_name

    current_text = callback.message.text

    updated_text = (
        f"{current_text}\n\n"
        f"✅ <b>Заявку взял в работу:</b> {manager_username}"
    )

    await callback.message.edit_text(
        text=updated_text,
        parse_mode="HTML",
        reply_markup=None
    )

    await callback.answer("Вы успешно взяли заявку в работу!", show_alert=True)

    try:
        await bot.send_message(
            chat_id=client_id,
            text=f"👋 Здравствуйте! Вашу заявку взял в работу наш менеджер {manager_username}. Напишет вам в ближайшее время!",
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Не удалось отправить уведомление клиенту: {e}")


# =====================================================================
# ЗАПУСК ИСПОЛНЕНИЯ
# =====================================================================

async def handle(request):
    return web.Response(text="Bot is running 24/7!")
async def main():
    print("Бот с интерактивными заявками успешно запущен!")
    async def main():
    # --- ДОБАВЛЯЕМ ЭТОТ БЛОК ДЛЯ RENDER ---
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    # --------------------------------------

    print("Бот с интерактивными заявками успешно запущен!")
    await dp.start_polling(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
