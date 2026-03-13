from typing import TypedDict

class MenuValue(TypedDict):
    text: str
    description: str

DESCRIPTION: dict[str, str] = {
    "about_description": """<b>🛒 SlyCart | Твой магазин</b>

Простой и быстрый доступ к товарам прямо в Telegram.

🔹 <b>Каталог</b> — всё актуальное наличие здесь.
🔹 <b>Удобство</b> — оформление заказа в пару кликов.
🔹 <b>Надежность</b> — твой комфорт наш приоритет.""",
    "tariff_description": """<b>💳 Тарифные планы SlyCart</b>

Выберите уровень мощности для вашего бизнеса:

🔹 <b>[Старт]</b> — 0₽
├ 10 товаров
└ Базовые кнопки

🚀 <b>[Бизнес]</b> — 990₽/мес
├ 100 товаров
├ <b>WebApp интерфейс</b>
└ Статистика продаж

🔥 <b>[Ультиматум]</b> — 2490₽/мес
├ ∞ товаров
├ Массовые рассылки
└ Приоритетная поддержка

<i>Нажмите на кнопку ниже, чтобы выбрать тариф.</i>""",
    "reg_description": "registration",
    "webapp": "tgwebapp"
}

TARIFF: dict[str, str] = {
    "free": "Бесплатный тариф",
    "advanced": "Тариф Бизнес",
    "premium": "Тариф Ультима"
}


MAIN_MENU: dict[str, MenuValue] = {
    "about": {"text" : "О нас", "description": DESCRIPTION['about_description']},
    "tariff": {"text": "Тарифы", "description": DESCRIPTION['tariff_description']},
    "reg": {"text": "Регистрация", "description": DESCRIPTION['reg_description']},
    "run_webapp": {"text": "Зайти в магазин", "description": DESCRIPTION['webapp']} 
}

if __name__ == "__main__":
    for menu_cb, menu in MAIN_MENU.items():
        print(menu_cb, menu['text'], menu['description']) 