import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pprint import pprint
from vk_api.utils import get_random_id
#from config import open_weather_token


def main():
    vk_session = vk_api.VkApi(token='467e9329e78d70b728147eb922f99675')
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.text:
            print('New from {}, text = {}'.format(event.user_id, event.text))

            if event.text.lower() == 'начать' or event.text.lower() == 'привет':
                user_name = vk.users.get(user_id=event.user_id)[0]['first_name']

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Привет, ' + user_name
                )

            if event.text.lower() == 'погода' or event.text.lower() == 'weather':
                city = "Москва"
                weather_message = get_weather(city, open_weather_token)

                if weather_message:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=weather_message
                    )


def get_bofort_scale(wind_speed):
    if wind_speed < 0.5:
        return "штиль"
    elif wind_speed < 1.6:
        return "очень лёгкий ветер"
    elif wind_speed < 3.4:
        return "лёгкий"
    elif wind_speed < 5.5:
        return "слабый"
    elif wind_speed < 8.0:
        return "умеренный"
    elif wind_speed < 10.8:
        return "свежий"
    elif wind_speed < 13.9:
        return "сильный"
    elif wind_speed < 17.2:
        return "крепкий"
    elif wind_speed < 20.8:
        return "очень крепкий"
    elif wind_speed < 24.5:
        return "шторм"
    elif wind_speed < 28.5:
        return "сильный шторм"
    elif wind_speed < 32.7:
        return "жёсткий шторм"
    else:
        return "ураган"


def get_wind_direction(deg):
    if deg < 22.5 or deg >= 337.5:
        return "северный"
    elif 22.5 <= deg < 67.5:
        return "северо-восточный"
    elif 67.5 <= deg < 112.5:
        return "восточный"
    elif 112.5 <= deg < 157.5:
        return "юго-восточный"
    elif 157.5 <= deg < 202.5:
        return "южный"
    elif 202.5 <= deg < 247.5:
        return "юго-западный"
    elif 247.5 <= deg < 292.5:
        return "западный"
    elif 292.5 <= deg < 337.5:
        return "северо-западный"
    else:
        return "неизвестное направление"


def get_weather(city, open_weather_token):
    weather_conditions = {
        "Clear": "ясно",
        "Clouds": "облачно",
        "Rain": "дождь",
        "Thunderstorm": "гроза",
        "Snow": "снег",
        "Mist": "туман"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data["name"]

        weather_description = data["weather"][0]["main"]
        if weather_description in weather_conditions:
            weather_desc = weather_conditions[weather_description]
        else:
            weather_desc = "ХЗ"

        cur_weather = data["main"]["temp_max"]
        cur_weather1 = data["main"]["temp_min"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        wind_direction_deg = data["wind"]["deg"]
        wind_direction = get_wind_direction(wind_direction_deg)
        bofort_scale = get_bofort_scale(wind_speed)

        return (
            f"Погода в Москве: {weather_desc}\n"
            f"Температура: {cur_weather}-{cur_weather1}°C\n"
            f"Давление: {pressure} мм рт. ст., влажность: {humidity}%\n"
            f"Ветер: {bofort_scale}, {wind_speed} м/с, {wind_direction}"
        )

    except Exception as ex:
        pass



