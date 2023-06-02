import json
import random
import re

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token, check_group_format
from parsing_links import week_number
from weather import *

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
upload = VkUpload(vk_session)
longpoll = VkLongPoll(vk_session)

# images
attachments = []
photo = upload.photo_messages(photos='src/ikbo-23-22.jpg')[0]
attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
photoes = ['src/ikbo-23-22.jpg', 'src/ikbo-23-22(2).jpg', 'src/ikbo-23-22(3).jpg', 'src/ikbo-23-22(4).jpg',
           'src/ikbo-23-22(5).jpg',
           'src/ikbo-23-22(6).jpg', 'src/ikbo-23-22(7).jpg', 'src/ikbo-23-22(8).jpg', 'src/ikbo-23-22(9).jpg',
           'src/ikbo-23-22(10).jpg']
doggo = upload.photo_messages(photos='src/ikbo-23-22.jpg')[0]

# weather API
weather_api_key = "ada08f64c3f4dfc5e5b043a59ed2bc6f"
weather_s = "{description}, температура: {temp_min}-{temp_max}\u00b0С\n" \
            "Давление: {pressure} мм рт.ст., влажность: {humidity}%\n" \
            "Ветер: {wind_character}, {wind_speed} м/с, {wind_direction}\n"
eng_to_rus = {"Thunderstorm": "гроза", "Drizzle": "морось", "Rain": "дождь", "Snow": "снег",
              "Mist": "туман", "Smoke": "смог", "Haze": "дымка", "Fog": "туман",
              "Dust": "пыль", "Sand": "песчаная буря", "Ash": "пепел",
              "Squall": "шквалистый ветер", "Tornado": "ураган",
              "Clouds": "облачно", "Clear": "ясно"}



# MIREA schedule
weekdays = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
todays_date = datetime.date.today()
group_regex = r"И[АВКНМ]{1}БО-[0-9]{2}-1[7-9]{1}"
current_group = ""
base_schedule_str = "Расписание на {weekday}, {date}:\n"


def is_group(group):
    return re.search(group_regex, group, re.IGNORECASE) is not None


# schedule for each course
with open("course1_sch.json", "r") as read_file:
    first_course_schedule = json.load(read_file)
with open("course2_sch.json", "r") as read_file:
    second_course_schedule = json.load(read_file)
with open("course2_sch.json", "r") as read_file:
    third_course_schedule = json.load(read_file)

oddity = 1 if int(week_number) % 2 == 0 else 0


def choose_random_photo():
    photo = upload.photo_messages(photos=random.choice(photoes))[0]
    return "photo{}_{}".format(photo["owner_id"], photo["id"])


def greeting(vk_event):
    # print('New from {}, text = {}'.format(vk_event.user_id, vk_event.text))
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message='Привет, ' + vk.users.get(user_id=vk_event.user_id)[0]['first_name'],
        keyboard=keyboard.get_keyboard(),
        attachment="photo{}_{}".format(doggo["owner_id"], doggo["id"])
    )


def instructions(vk_event):
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message='Инструкция по работе с ботом:\n'
                'Этот бот умеет выдавать расписание студентов ИИТ РТУ МИРЭА и сообщать о погоде. '
                'Для каждого раздела есть свои команды. Чтобы увидеть список доступных команд (кнопки) в любое время, отправьте сообщение "бот".\n\n'
                'Список команд бота:\n\n'
                '"Ковид" - статистика по заболеваниям в России за последние сутки и график заболевамости за последние 10 дней,\n\n'
                'Название группы в формате "ИXБО-XX-XX" - основная группа, по которой будет выдаваться расписание (необходимо набирать каждый раз при заходе в диалог с ботом),\n\n'
                '"Какая группа?" - основная группа на данный момент,\n\n'
                '"Какая неделя?" - номер текущей недели, \n\n'
                '"Расписание на сегодня", "Расписание на завтра", "Расписание на эту неделю", "Расписание на следующую неделю" - подробное расписание занятий на соответствующий период,\n\n'
                '"Бот <группа>" - изменить основную группу и показать ее расписание на выбранный период,\n\n'
                '"Бот <день недели>" - расписание для нечетной и четной недели в соответствующий день у основной группы,\n\n'
                '"Бот <день недели> <группа>" - расписание для нечетной и четной недели в соответствующий день у указанной группы,\n\n'
                '"Погода" - погода в Москве на выбранный период времени.\n\n'

                'Если команда не будет совпадать со списком перечисленных, бот кинет обидку. Удачи!',
    )


def show_functions(vk_event):
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message="Показать...",
        keyboard=keyboard.get_keyboard()
    )


def unknown(vk_event):
    vk.messages.send(
        user_id=vk_event.user_id,
        attachment=','.join(attachments),
        random_id=get_random_id(),
        message='Неизвестная команда. Чтобы посмотреть список допустимых команд, отправьте "инструкция" или "бот"'
    )


def set_current_group(vk_event, group):
    global current_group
    current_group = str(group).upper()
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message="Я запомнил, что ты из группы " + current_group,
        keyboard=keyboard.get_keyboard()
    )


def print_current_group(vk_event):
    if current_group == "":
        s = "Сначала введите номер группы"
    else:
        s = "Показываю расписание группы " + current_group.upper()

    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message=s,
        keyboard=keyboard.get_keyboard()
    )


def print_current_week(vk_event):
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message='Идёт ' + str(week_number) + ' неделя',
        keyboard=keyboard.get_keyboard()
    )


def choose_schedule(group):
    if group.endswith("22"):
        return first_course_schedule
    elif group.endswith("21"):
        return second_course_schedule
    elif group.endswith("20"):
        return third_course_schedule


def day_schedule(group, day=todays_date, for_next_week=False):
    # Определение дня недели (weekday) и форматирование даты и дня недели
    current_weekday = day.weekday()
    current_weekday_s = weekdays[current_weekday]
    inner_oddity = oddity

    # Если указано расписание на следующую неделю, то меняем значене внутренней переменной "oddity"
    # (которая используется для выбора пар в текущей неделе) на противоположное
    if for_next_week:
        inner_oddity = 1 if oddity == 0 else 0

    # Формируем строку с данными о дате и дне недели
    s = base_schedule_str.format(
        weekday=current_weekday_s.replace("а", "у") if current_weekday_s.endswith("а") else current_weekday_s,
        date=day.strftime('%d.%m.%Y'))

    # Если не было указаноазвания группы, возвращаем сообщение об ошибке
    if group == "":
        s = "Сначала введите номер группы"
    else:
        # Получим расписание выбранной группы, используя функцию choose_schedule
        curr_schedule = choose_schedule(group)

        lesson_num = 0

        try:
            # Проверяем, что не воскресенье (т.к. воскресенье - отдельный случай)
            if current_weekday != 6:
                # Проходимся по каждой паре в текущий день и добавляем в строку s
                for i in range(7):
                    lesson_num += 1
                    day_info = list(curr_schedule[group.upper()][current_weekday_s][i][inner_oddity].values())
                    s += str(lesson_num) + ") " + ', '.join(day_info) + '\n'
            else:
                # Если воскресенье, добавляем только информацию для этого дня из расписания текущей группы
                s += str(curr_schedule[group.upper()][current_weekday_s])
        except KeyError:
            # В случае, если название группы указано неверно, возвращаем сообщение об ошибке
            s = "Группы не существует или для нее отсутствует расписание. " \
                "Пожалуйста, отправьте корректное название группы"

    # Возвращаем сформированную строку
    return s


def print_day_schedule(vk_event, group, day=todays_date, next_week=False):
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message=day_schedule(group, day, for_next_week=next_week),
        keyboard=keyboard.get_keyboard()
    )


def print_week_schedule(vk_event, group, next_week=False):
    msg = ""
    if next_week:
        dates = [todays_date + datetime.timedelta(days=i) for i in
                 range(7 - todays_date.weekday(), 14 - todays_date.weekday())]
    else:
        dates = [todays_date + datetime.timedelta(days=i) for i in
                 range(0 - todays_date.weekday(), 7 - todays_date.weekday())]

    for day in dates:
        if msg != "Сначала введите номер группы\n":
            msg += day_schedule(group, day=day, for_next_week=next_week) + '\n'

    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message=msg
    )


def weekday_schedule(vk_event, weekday, group):
    msg = ""
    if group == "":
        msg += "Сначала введите номер группы"
    else:
        msg += weekday.capitalize() + ", нечетная неделя:\n"
        curr_sch = choose_schedule(group)
        lesson_num = 0
        try:
            if weekday != "воскресенье":
                for i in range(6):  # amount of lessons
                    lesson_num += 1
                    day_info = list(curr_sch[group][weekday][i][0].values())
                    msg += str(lesson_num) + ") " + ', '.join(day_info) + '\n'
            else:
                msg += curr_sch[group][weekday]

            msg += "\n" + weekday.capitalize() + ", четная неделя:\n"
            lesson_num = 0

            if weekday != "воскресенье":
                for i in range(6):  # amount of lessons
                    lesson_num += 1
                    day_info = list(curr_sch[group][weekday][i][1].values())
                    msg += str(lesson_num) + ") " + ', '.join(day_info) + '\n'
            else:
                msg += curr_sch[group][weekday]
        except KeyError:
            msg = "Группы не существует или для нее отсутствует расписание. " \
                  "Пожалуйста, отправьте корректное название группы"

    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message=msg
    )


def change_group(vk_event, group):
    global current_group
    current_group = group.upper()
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message="Показать расписание группы " + group.upper() + "...",
        keyboard=keyboard.get_keyboard()
    )


# BOT APPEARANCE AND BEHAVIOUR

# Buttons
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Расписание на сегодня', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Расписание на завтра', color=VkKeyboardColor.NEGATIVE)
keyboard.add_line()  # Добавляем новую строку
keyboard.add_button('На эту неделю', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('На следующую неделю', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()  # Добавляем новую строку
keyboard.add_button('Какая неделя?', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Какая группа?', color=VkKeyboardColor.SECONDARY)

# Mainloop
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg_words = event.text.lower().split()
        if event.text.lower() == "начать":
            greeting(event)
            instructions(event)
        elif event.text.lower() == "привет":
            greeting(event)
        elif event.text.lower() == "инструкция":
            instructions(event)
        elif event.text.lower() == "расписание на сегодня":
            print_day_schedule(event, current_group)
        elif event.text.lower() == "на эту неделю":
            print_week_schedule(event, current_group)
        elif event.text.lower() == "на следующую неделю":
            print_week_schedule(event, current_group, next_week=True)
        elif event.text.lower() == "расписание на завтра":
            if todays_date.weekday() != 6:
                print_day_schedule(event, current_group, todays_date + datetime.timedelta(days=1))
            else:
                print_day_schedule(event, current_group, todays_date + datetime.timedelta(days=1), next_week=True)
        elif event.text.lower() == "какая группа?":
            print_current_group(event)
        elif event.text.lower() == "какая неделя?":
            print_current_week(event)
        elif len(msg_words) == 1 and check_group_format(msg_words[0]):
            set_current_group(event, event.text)
        elif msg_words[0] == "бот":
            if len(msg_words) == 1:
                show_functions(event)
            if len(msg_words) == 2:
                if msg_words[1] in weekdays:
                    weekday_schedule(event, msg_words[1], current_group)
                elif is_group(msg_words[1]):
                    change_group(event, msg_words[1])
            elif len(msg_words) == 3:
                if msg_words[1] in weekdays and is_group(msg_words[2]):
                    weekday_schedule(event, msg_words[1], msg_words[2].upper())
        elif event.text.lower() == "погода" or event.text.lower() == "погоду":
            weather_keyboard(event)
        elif event.text.lower() == "сейчас":
            current_weather(event)
        elif event.text.lower() == "сегодня":
            day_weather(event)
        elif event.text.lower() == "завтра":
            day_weather(event, next_day=True)
        elif event.text.lower() == "на 5 дней":
            week_weather(event)
        elif event.text.lower() == "спасибо" or event.text.lower() == "спс" or event.text.lower() == "молодец":
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                attachment=choose_random_photo()
            )
        else:
            unknown(event)
