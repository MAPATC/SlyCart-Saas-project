DESCRIPTION: dict[str, str] = {
    "about_description": "Прикольное название(потом)",
    "tariff_description": "Тарифы(чуть позже)",
    "reg_description": "registration",
    "webapp": "tgwebapp"
}


MAIN_MENU: dict[str, dict[str, str]] = {
    "about": {"text" : "О нас", "description": DESCRIPTION['about_description']},
    "tariff": {"text": "Тарифы", "description": DESCRIPTION['tariff_description']},
    "reg": {"text": "Регистрация", "description": DESCRIPTION['reg_description']},
    "run_webapp": {"text": "Зайти в магазин", "description": DESCRIPTION['webapp']} 
}