from confidential import Confidential as Con_data
from DialogTree import DialogTree
from BaseFunc import BaseFunc
from EmailHandler import EmailHandler
import time

# from telegram import User

# Определение константы для текста "В начало"
START_TEXT = "В начало"


class BotLogic(BaseFunc):
    def __init__(self, token):
        super().__init__(token)
        self.chat_states = {}

    def handle_start(self, message):
        chat_id = message.chat.id
        self.send_start_message(chat_id)

    def send_start_message(self, chat_id):
        self.chat_states[chat_id] = {'current_state': self.start_menu_btn(DialogTree.telegram_bot_data)}
        keyboard = self.create_keyboard(self.chat_states[chat_id]['current_state'])
        self.send_message(chat_id, "Добро пожаловать в автоматизированную справочную систему Университета "
                                   "Вернадского! Вы можете найти в нашем боте основную информацию для "
                                   "абитуриентов/студентов, ссылки на электронные ресурсы и ЭИОС, а также задать "
                                   "любой интересующий Вас вопрос через систему обращений! Просто выбирайте нужный "
                                   "пункт через кнопки в нижней части экрана! Если вдруг их не видно, пожалуйста, "
                                   "наберите в текстовой строке «/start» (без кавычек!). Спасибо за Ваше участие в "
                                   "жизни Университета! Мы продолжаем работу и совершенствуем нашего бота!",
                          reply_markup=keyboard)

    def handle_custom_message_email(self, message, to_email):
        chat_id = message.chat.id
        text = message.text

        # Получаем данные о пользователе
        user = message.from_user
        user_info = f"Имя: {user.first_name}\nФамилия: {user.last_name}\nUsername: {user.username}\nChat ID: {chat_id}"

        if chat_id not in self.chat_states:
            self.send_start_message(chat_id)
            return

        if 'waiting_for_contact_info' not in self.chat_states[chat_id]:
            # Пользователь только что выбрал отправку письма, просим описать вопрос
            self.chat_states[chat_id]['waiting_for_contact_info'] = True
            self.chat_states[chat_id]['custom_message'] = text
            keyboard = self.create_keyboard(
                self.chat_states[chat_id]['current_state'] + [START_TEXT])  # Добавлено здесь
            self.send_message(chat_id, "Пожалуйста, в ОДНОМ сообщении, оставьте свои контактные данные (почту в "
                                       "формате xxxxxxx@xxxxxxx.xx, на неё Вам придёт ответ, и телефон в формате "
                                       "+7XXXXXXXXXX, по нему мы постараемся с Вами связаться, если Вы ошибётесь в "
                                       "почте) и кратко опишите интересующий Вас вопрос "
                                       "ВАЖНО: В рамках данного запроса Вы соглашаетесь на предоставление службам "
                                       "Университета своих  контактных данных, без передачи этой информации третьим "
                                       "лицам!", reply_markup=keyboard)  # И здесь
        else:

            # Создаем экземпляр EmailHandler
            smtp_server = Con_data.smtp_server
            smtp_port = Con_data.smtp_port
            smtp_username = Con_data.smtp_username
            smtp_password = Con_data.smtp_password
            from_email = Con_data.smtp_username

            email_handler = EmailHandler(smtp_server, smtp_port, smtp_username, smtp_password, from_email)

            # Отправляем сообщение с контактами через EmailHandler
            custom_message = f"{self.chat_states[chat_id]['custom_message']}\n\nUser Info:\n{user_info}"

            if EmailHandler.has_contact_info(text):
                if email_handler.send_email(to_email, "Вопрос от пользователя", custom_message, text):
                    self.send_message(chat_id, "Спасибо за Ваше обращение и интерес к Университету! В ближайшее время "
                                               "Вам придёт ответ на указанный адрес электронной почты!")

                    # Очищаем состояние чата
                    del self.chat_states[chat_id]['waiting_for_contact_info']
                    del self.chat_states[chat_id]['custom_message']
                else:
                    print(f"DEBUG: Ошибка при отправке письма - Chat ID: {chat_id}")  # Добавлено для отладки
                    self.send_message(chat_id, "Произошла ошибка при отправке вопроса. Попробуйте позже.")
            else:
                self.send_message(chat_id, "Пожалуйста, укажите ваш вопрос и контактные данные (номер телефона и email)"
                                           "в одном сообщении для отправки вашего вопроса.")

    def handle_message(self, message):
        chat_id = message.chat.id
        text = message.text

        if chat_id not in self.chat_states:
            self.send_start_message(chat_id)
            return

        current_state = self.chat_states[chat_id]['current_state']

        if text == START_TEXT:
            self.send_start_message(chat_id)
        elif text == "Назад":
            if len(current_state) > 1:
                current_state.pop()
            self.chat_states[chat_id]['current_state'] = current_state
            self.send_message(chat_id, "Выберите следующий шаг:",
                              reply_markup=self.create_keyboard(current_state + [START_TEXT]))
        elif text.startswith("Написать письмо в университет"):
            to_email = Con_data.vuz_mail
            self.handle_custom_message_email(message, to_email)
            self.chat_states[chat_id]['waiting_for_contact_info'] = False
        elif 'waiting_for_contact_info' in self.chat_states[chat_id]:
            # Обработка сообщения пользователя после запроса контактных данных
            to_email = Con_data.vuz_mail
            self.handle_custom_message_email(message, to_email)
        else:
            next_state = self.find_btn_text(DialogTree.telegram_bot_data, text)

            if next_state:
                current_state.append(text)
                self.chat_states[chat_id]['current_state'] = next_state
                keyboard = self.create_keyboard(next_state + [START_TEXT])
                self.send_message(chat_id, "Выберите следующий шаг:", reply_markup=keyboard)
            else:
                response = self.find_value(DialogTree.telegram_bot_data, text)
                if response:
                    keyboard = self.create_keyboard([START_TEXT])
                    self.send_message(chat_id, response, reply_markup=keyboard)
                else:
                    self.send_message(chat_id, "Извините, но я не могу ответить на ваш вопрос.")

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start_command(message):
            self.handle_start(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            self.handle_message(message)

        self.bot.polling(none_stop=True, interval=0.1)


if __name__ == "__main__":
    token_value = Con_data.token_value

    while True:
        try:
            my_bot = BotLogic(token_value)
            my_bot.run()
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            print("Перезапуск через 2 секунды...")
            time.sleep(2)
