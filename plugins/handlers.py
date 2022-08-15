import asyncio
import requests
from pyrogram import Client, filters, enums
import json


async def is_greetings(_, __, query):
    return query.text == "Hi"


greetings_filter = filters.create(is_greetings)


async def is_gratitude(_, __, query):
    return query.text == "Thanks" or query.text == "Thank you"


gratitudes_filter = filters.create(is_gratitude)


def state_icon(code, client, message):
    url = 'https://openweathermap.org/img/wn/{code}@2x.png'
    response = requests.post(url)


def parse_weather_data(data):
    for elem in data['weather']:
        weather_state = elem['main']
        icon = elem['icon']
    temp = round(data['main']['temp'] - 273.15, 2)
    city = data['name']
    msg = f'The weather in {city}: Temp is {temp}, State is {weather_state}'
    return msg, icon


def get_weather(location):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}'.format(city=location,
                                                                                          token='c658050b4f89b7f4f2120fdb66c61834')
    response = requests.get(url)
    if response.status_code != 200:
        return 'city not found'
    data = json.loads(response.content)
    return parse_weather_data(data)


@Client.on_message(filters.command(['start', '/start']))
async def start_handler(client, message):
    await asyncio.sleep(3)
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    await asyncio.sleep(5)
    await client.send_message(message.chat.id, "Hey, you've just started me. Print 'Hi' to see my abilities")


@Client.on_message(filters.command(['end']))
async def end_handler(client, message):
    await asyncio.sleep(3)
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    await asyncio.sleep(5)
    await client.send_message(message.chat.id, "Goodbye, write me later")
    await asyncio.sleep(5)
    for m_ids in reversed(range(message.id - 200, message.id + 4)):
        try:
            await client.delete_messages(
                message.chat.id,
                m_ids
            )
        except Exception as e:
            client.send_message(
                message.chat.id,
                f"An error occurred: {e}"
            )
            break  # Excepts errors given by Telegram, like floodwaits


@Client.on_message(filters.text & greetings_filter)
async def greetings_handler(client, message):
    await asyncio.sleep(3)
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    await asyncio.sleep(5)
    await client.send_message(message.chat.id,
                              "Hello, I can send you current weather in your city. Please, write your city")


@Client.on_message(filters.text & gratitudes_filter)
async def gratitude_handler(client, message):
    await asyncio.sleep(3)
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    await asyncio.sleep(5)
    await client.send_message(message.chat.id, "You are welcome")


@Client.on_message(filters.text)
async def text_handler(client, message):
    await asyncio.sleep(3)
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    await asyncio.sleep(5)
    data = get_weather(message.text)
    # await client.send_message(message.text, get_weather(message.text))
    await client.send_message(message.chat.id, data[0])
    await client.send_photo(message.chat.id, f'https://openweathermap.org/img/wn/{data[1]}@2x.png')


@Client.on_message(filters.sticker)
async def sticker_handler(client, message):
    await asyncio.sleep(3)
    await client.send_chat_action(message.chat.id, enums.ChatAction.CHOOSE_STICKER)
    await asyncio.sleep(5)
    print(message)
    await client.send_sticker(message.chat.id, message.sticker.file_id)
