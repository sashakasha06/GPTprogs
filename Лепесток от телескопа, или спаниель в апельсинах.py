import json
import sys
from openai import OpenAI

client = OpenAI(
    api_key="sk-79GgdKZzhyOK8rvnpciFogWX3yA61T5W",
    base_url="https://api.proxyapi.ru/openai/v1",
)
words = []
for line in sys.stdin:
    words.append(line.rstrip('\n'))
messages = []
result = ', '.join(words)
promt = 'Имеются следующие входные данные: "' + result + '''". Выведи количество слов и сами слова(в том же порядке, в котором они упоминаются в списке) из этого списка, которые можно составить с помощью букв первого слова. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: {
  "число": 3,
  "слова": ["лес", "весло", "сопло"]
}'''
print(promt)
messages.append({"role": "user", "content": promt})
chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=1000
)
response_text = chat_completion.choices[0].message.content
modified_text = response_text.replace('```', '').replace('json', '')
planets = json.loads(modified_text)
print(planets["число"])
for value in planets["слова"]:
    print(value)
messages.append({"role": "assistant", "content": response_text})