import telebot
from telebot import types


class BaseFunc:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def send_message(self, chat_id, text, reply_markup=None):
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    @staticmethod
    def create_keyboard(buttons):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button_text in buttons:
            keyboard.add(types.KeyboardButton(text=button_text))
        return keyboard

    @staticmethod
    def find_btn_text(work_dict, key=None):
        for current_key, value in work_dict.items():
            if isinstance(value, dict):
                if key is not None and key == current_key:
                    return list(value.keys())  # Возвращаем список ключей из вложенного словаря
                result = BaseFunc.find_btn_text(value, key)
                if result is not None:
                    return result

    @staticmethod
    def find_value(work_dict, key):
        for current_key, value in work_dict.items():
            if current_key == key:
                if isinstance(value, dict):
                    return None  # Если значение - это словарь, возвращаем None
                else:
                    return value  # Возвращаем значение
            elif isinstance(value, dict):
                result = BaseFunc.find_value(value, key)
                if result is not None:
                    return result
        return None

    @staticmethod
    def start_menu_btn(work_dict):
        root_keys = list(work_dict.keys())  # Получаем список корневых ключей
        return root_keys
