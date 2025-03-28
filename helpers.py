import random
import string

def generate_random_string(length):
    """Генерирует случайную строку заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_phone_number():
    """Генерирует случайный номер телефона jn """
    return "+7" + ''.join(random.choice(string.digits) for i in range(10, 12))

def generate_random_rent_time():
    """Генерирует случайное количество дней аренды (от 1 до 7)."""
    return random.randint(1, 7)

def generate_random_date():
    """Генерирует случайную дату от 2025-04-01 до 2025-12-30"""
    return "2025-"+ str(random.randint(4,12))+"-" + str(random.randint(10, 30))

def generate_random_metro_station():
    """Генерирует случайное количество дней аренды (от 1 до 7)."""
    metro_stations = ["Сокольники", "Комсомольская", "Красные ворота", "Чистые пруды", "Лубянка"]
    return random.choice(metro_stations)

