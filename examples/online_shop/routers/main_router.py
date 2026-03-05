from core.bot import Bot
from core.events import EventMessageCreated, EventMessageCallback
from core.handlers.router import Router
from core.keyboards import Keyboard, ButtonCallback


router = Router()


def build_main_menu() -> Keyboard:
    keyboard = Keyboard()
    keyboard.add_button(ButtonCallback("🛍 Каталог", "menu_catalog"))
    keyboard.add_button(ButtonCallback("🧺 Корзина", "menu_cart"))
    keyboard.add_button(ButtonCallback("ℹ Контакты", "menu_contacts"))
    return keyboard


@router.message()
async def handle_start(event: EventMessageCreated, bot: Bot):
    """
    Простой пример «онлайн‑магазина»:
    по любому входящему сообщению показываем главное меню.
    """
    message = event.message
    keyboard = build_main_menu()
    await bot.send(
        "Добро пожаловать в наш онлайн‑магазин!\n"
        "Выберите раздел из меню ниже 👇",
        [keyboard.get_keyboard()],
        user_id=message.sender.user_id,
    )


@router.callback_query()
async def handle_menu_callbacks(event: EventMessageCallback, bot: Bot):
    callback = event.callback
    payload = callback.payload
    user_id = callback.user.user_id

    if payload == "menu_catalog":
        keyboard = Keyboard()
        keyboard.add_button(ButtonCallback("💻 Ноутбуки", "catalog_laptops"))
        keyboard.add_button(ButtonCallback("📱 Смартфоны", "catalog_phones"))
        keyboard.add_button(ButtonCallback("⬅ Назад", "menu_back"))
        text = "Каталог товаров:\n\nВыберите категорию:"

    elif payload == "menu_cart":
        keyboard = Keyboard()
        keyboard.add_button(ButtonCallback("⬅ Назад в меню", "menu_back"))
        text = "Ваша корзина пока пуста.\nДобавьте товар из каталога 🙂"

    elif payload == "menu_contacts":
        keyboard = Keyboard()
        keyboard.add_button(ButtonCallback("⬅ Назад в меню", "menu_back"))
        text = (
            "Контакты магазина:\n"
            "E‑mail: support@example.com\n"
            "Телефон: +7 (999) 123‑45‑67"
        )

    elif payload in {"catalog_laptops", "catalog_phones"}:
        keyboard = Keyboard()
        keyboard.add_button(ButtonCallback("🧺 В корзину", "cart_add_dummy"))
        keyboard.add_button(ButtonCallback("⬅ К каталогу", "menu_catalog"))
        category = "ноутбуков" if payload == "catalog_laptops" else "смартфонов"
        text = (
            f"Популярные модели {category}:\n"
            "- Модель 1\n"
            "- Модель 2\n"
            "- Модель 3"
        )

    elif payload == "cart_add_dummy":
        keyboard = Keyboard()
        keyboard.add_button(ButtonCallback("⬅ В меню", "menu_back"))
        text = "Товар добавлен в корзину (демо).\nПерейдите в раздел «Корзина», чтобы посмотреть."

    elif payload == "menu_back":
        keyboard = build_main_menu()
        text = "Главное меню магазина:"

    else:
        keyboard = build_main_menu()
        text = "Неизвестная команда. Показано главное меню:"

    await bot.send(
        text,
        [keyboard.get_keyboard()],
        user_id=user_id,
    )


