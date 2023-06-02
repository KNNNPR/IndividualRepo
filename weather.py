import datetime
import math
import PIL.Image as Image
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from config import weather_api_key
from vk_part import weather_s, todays_date, eng_to_rus, upload, vk


def wind_degrees_to_name(degree):
    if 0 <= degree < 45 or degree == 360:
        return "северный"
    elif 45 <= degree < 90:
        return "северо-восточный"
    elif 90 <= degree < 135:
        return "восточный"
    elif 135 <= degree < 180:
        return "юго-восточный"
    elif 180 <= degree < 225:
        return "южный"
    elif 225 <= degree < 270:
        return "юго-западный"
    elif 270 <= degree < 315:
        return "западный"
    elif 315 <= degree < 360:
        return "северо-западный"


def wind_speed_to_desc(speed):
    if 0 <= speed < 0.3:
        return "штиль"
    elif 0.3 <= speed < 3.3:
        return "легкий"
    elif 3.4 <= speed < 5.5:
        return "слабый"
    elif 5.5 <= speed < 10.8:
        return "умеренный"
    elif 10.8 <= speed < 20.8:
        return "сильный"
    elif 20.8 <= speed < 32.7:
        return "шторм"
    elif speed >= 32.7:
        return "ураган"


def pressure_in_mm(pressure):
    return math.floor(pressure * 100 / 133)


def current_weather(vk_event):
    weather_site = "http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=" + weather_api_key + "&units=metric&lang=ru"
    weather_response = requests.get(weather_site)
    weather_info = weather_response.json()

    new_s = weather_s.format(description=weather_info["weather"][0]["description"].capitalize(),
                             temp_min=round(weather_info["main"]["temp_min"]),
                             temp_max=round(weather_info["main"]["temp_max"]),
                             pressure=pressure_in_mm(weather_info["main"]["pressure"]),
                             humidity=weather_info["main"]["humidity"],
                             wind_character=wind_speed_to_desc(weather_info["wind"]["speed"]),
                             wind_speed=round(weather_info["wind"]["speed"]),
                             wind_direction=wind_degrees_to_name(weather_info["wind"]["deg"]))

    image = requests.get("http://openweathermap.org/img/w/" + weather_info["weather"][0]["icon"] + ".png", stream=True)

    with open("single.png", "wb") as f:
        f.write(image.content)

    weather_pic = upload.photo_messages(photos='single.png')[0]
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message="Погода в Москве: {main}\n".format(main=eng_to_rus[weather_info["weather"][0]["main"]]),
        attachment="photo{}_{}".format(weather_pic["owner_id"], weather_pic["id"])
    )
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message=new_s
    )


def day_weather(vk_event, next_day=False):
    weath = ""
    weather_site = "http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid=" + weather_api_key + "&units=metric&lang=ru"
    weather_response = requests.get(weather_site)
    weather_info = weather_response.json()
    start_index = 0
    img = Image.new('RGB', (200, 50))
    pic_x = 0

    if next_day:
        for i in range(9):
            if int(weather_info["list"][i]["dt_txt"].split()[1].split(':')[0]) == 0 and i != 0:
                start_index = i

    for daytime in range(start_index, start_index + 7, 2):
        hour = int(weather_info["list"][daytime]["dt_txt"].split()[1].split(':')[0])
        if 0 <= hour < 6:
            weath += "------------------НОЧЬ------------------\n"
        elif 6 <= hour < 12:
            weath += "------------------УТРО------------------\n"
        elif 12 <= hour < 18:
            weath += "------------------ДЕНЬ------------------\n"
        elif 18 <= hour < 24:
            weath += "------------------ВЕЧЕР------------------\n"

        image = requests.get(
            "http://openweathermap.org/img/w/" + weather_info["list"][daytime]["weather"][0]["icon"] + ".png",
            stream=True)
        with open("file_.png", "wb") as f:
            f.write(image.content)
        img_pt = Image.open("file_.png")
        img.paste(img_pt, (pic_x, 0))
        pic_x += 50

        weath += weather_s.format(
            description=weather_info["list"][daytime]["weather"][0]["description"].capitalize(),
            temp_min=round(weather_info["list"][daytime]["main"]["temp_min"]),
            temp_max=round(weather_info["list"][daytime]["main"]["temp_max"]),
            pressure=pressure_in_mm(weather_info["list"][daytime]["main"]["pressure"]),
            humidity=weather_info["list"][daytime]["main"]["humidity"],
            wind_character=wind_speed_to_desc(weather_info["list"][daytime]["wind"]["speed"]),
            wind_speed=round(weather_info["list"][daytime]["wind"]["speed"]),
            wind_direction=wind_degrees_to_name(weather_info["list"][daytime]["wind"]["deg"]))
        weath += "\n"

    # pprint(weather_info)

    img.save("day_weather.png")
    weather_pic = upload.photo_messages(photos='day_weather.png')[0]

    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message="Погода в Москве на {day}".format(day="завтра" if next_day else "сегодня"),
        attachment="photo{}_{}".format(weather_pic["owner_id"], weather_pic["id"])
    )

    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message=weath
    )


def week_weather(vk_event):
    weather = ""
    weather_site = "http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid=" + weather_api_key + "&units=metric&lang=ru"
    weather_response = requests.get(weather_site)
    weather_info = weather_response.json()
    # pprint(weather_info)
    night_start_index = 0
    day_start_index = 0
    start_pic_x = 0

    img = Image.new('RGB', (250, 50))

    for i in range(9):
        if int(weather_info["list"][i]["dt_txt"].split()[1].split(':')[0]) == 0:
            night_start_index = i
        if int(weather_info["list"][i]["dt_txt"].split()[1].split(':')[0]) == 12:
            day_start_index = i

    for day in range(day_start_index, len(weather_info["list"]), 8):
        weather += "/ " + str(round(weather_info["list"][day]["main"]["temp"])) + "\u00b0С /"

        image = requests.get(
            "http://openweathermap.org/img/w/" + weather_info["list"][day]["weather"][0]["icon"] + ".png",
            stream=True)
        with open("file.png", "wb") as f:
            f.write(image.content)
        img_part = Image.open("file.png")
        img.paste(img_part, (start_pic_x, 0))
        start_pic_x += 50

    img.save("week_weather.png")
    weather_pic = upload.photo_messages(photos='week_weather.png')[0]

    weather += " ДЕНЬ\n"

    for night in range(night_start_index, len(weather_info["list"]), 8):
        weather += "/  " + str(round(weather_info["list"][night]["main"]["temp"])) + "\u00b0С /"

    weather += " НОЧЬ"

    period_end = todays_date + datetime.timedelta(days=5)

    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message="Погода в Москве c {start_day} до {end_day}".format(start_day=todays_date.strftime("%d.%m"),
                                                                    end_day=period_end.strftime("%d.%m")),
        attachment="photo{}_{}".format(weather_pic["owner_id"], weather_pic["id"])
    )

    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message=weather
    )


def weather_keyboard(vk_event):
    temp_keyboard = VkKeyboard(one_time=True)
    temp_keyboard.add_button(label='сейчас', color=VkKeyboardColor.PRIMARY)
    temp_keyboard.add_button(label='сегодня', color=VkKeyboardColor.POSITIVE)
    temp_keyboard.add_button(label='завтра', color=VkKeyboardColor.POSITIVE)
    temp_keyboard.add_line()
    temp_keyboard.add_button(label='на 5 дней', color=VkKeyboardColor.POSITIVE)
    vk.messages.send(
        user_id=vk_event.user_id,
        random_id=get_random_id(),
        message="Показать погоду в Москве",
        keyboard=temp_keyboard.get_keyboard()
    )
