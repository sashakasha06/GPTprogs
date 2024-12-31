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
# далек	далеки
# далека	далеков
# далеку	далекам
# далека
# далеком	далеками
# (о) далеке	(о) далеках
promt = 'Имеются следующие входные данные: "' + result + '''". Выведи количество строк, в которых встречается слово "Далек"(Но не "далеко") в любом числе и падеже(Именительный, родительный, дательный, винительный, творительный и предложный). Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: 3'''
messages.append({"role": "user", "content": promt})
chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=1000
)
response_text = chat_completion.choices[0].message.content
modified_text = response_text.replace('```', '').replace('json', '')
planets = json.loads(modified_text)
print(response_text)
#messages.append({"role": "assistant", "content": response_text})