class DialogTree:
    # Система словарей для телеграм-бота
    # не менять ветки: "Отправить письмо в приёмную комиссию", "Написать письмо в ВУЗ".
    telegram_bot_data = {
        "Поступление в ВУЗ": {
            "Поступление через сервис ГосУслуги": "Переходите по ссылке и следуйте инструкциям сайта "
                                                  "https://www.gosuslugi.ru/vuzonline",
            "Адрес приёмной комиссии": "143907, Московская область, г. Балашиха, Шоссе Энтузиастов 50, каб 116. Часы "
                                       "работы: пн-чт 9:00-18:00, пт 9:00-16:45",
            "Связаться с приёмной комиссией": {
                "Часы работы приёмной комиссии (звоните в рабочие часы)": "Пн-Чт 09:00-18:00, Пт 09:00-16:45, Сб ("
                                                                          "только во время приёмной компании) "
                                                                          "09:00-13:00. Обеденное время 13:00-14:00",
                "Позвонить в приёмную комиссию": "Вы можете связаться с приёмной комиссией по телефону 8 (495) "
                                                 "521-55-46",
                "Отправить письмо в приёмную комиссию": None
            }
        },
        "Занятия в режиме online": {
            "Личный кабинет абитуриента/студента": "https://lk.rgunh.ru/login",
            "Личный кабинет ЭИОС": "Все Ваши занятия в дистанционном формате Вы можете найти здесь - "
                                   "https://portfolio.rgunh.ru/login/index.php",
            "ЭИОС (Электронная информационно-образовательная среда)": "https://portfolio.rgunh.ru/",
            "Официальное мобильное приложение вуза": "Мы уже работаем над тем, чтобы Вам было удобно следить за "
                                                     "своими успехами. Подождите ещё немного"
        },
        "Информационные ресурсы вуза": {
            "Сайт вуза": "Всю необходимую информацию для абитуриентов, студентов и преподавателей можно найти на "
                         "rgunh.ru",
            "Официальная группа вуза в ВКонтакте": "Последние новости вуза, интересные видеоматериалы и трансляции! "
                                                   "https://vk.com/rgunh",
            "Официальный канал вуза в telegram": "Все важные события в удобном формате! https://t.me/rgunhru"
        },
        "У Вас ещё остались вопросы?": {
            "Написать письмо в ВУЗ": None
        }
    }
