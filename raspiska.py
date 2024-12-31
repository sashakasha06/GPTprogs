import json
import sys
from openai import OpenAI

client = OpenAI(
    api_key="sk-79GgdKZzhyOK8rvnpciFogWX3yA61T5W",
    base_url="https://api.proxyapi.ru/openai/v1",
)
messages = []
words = []
for line in sys.stdin:
    if line != '\n':
        words.append(line.rstrip('\n'))
print(words)
result = ', '.join(words)
print(result)
promt = 'Имеются следующие входные данные: ' + result + '''. Найди строки, содержащие в себе любую из цифр(1, 2, 3, 4, 5, 6, 7, 8, 9, 0), в том числе и несколько. Создай словарь, в котором ключом будут числа, а значением - текст. Если значение уже есть в словаре, то заносить его вновь не надо. Выведи этот словарь. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: {"5": Математика, "10": [Музыка, Английский язык], "9": Русский язык}'''
messages.append({"role": "user", "content": promt})
chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=1000
)
response_text = chat_completion.choices[0].message.content
modified_text = response_text.replace('```', '').replace('json', '')
planets = json.loads(modified_text)
for key, value in planets.items():
    print(key, ': ', value)
messages.append({"role": "assistant", "content": response_text})