import os
import time
from functools import update_wrapper

import requests
from dotenv import load_dotenv

load_dotenv()

# Acessa as variáveis de ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN", "")
URL = f"https://api.telegram.org/bot{TOKEN}/"


def get_updates(last_update_id=None):
    url = URL + "getUpdates?timeout=100"
    if last_update_id:
        url += f"&offset={last_update_id}"
    response = requests.get(url)
    return response.json()


def send_message(chat_id, text):
    url = URL + f"sendMessage?chat_id={chat_id}&text={text}"

    response = requests.get(url)
    x = response.json()
    print(x)
    return x


def main():
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        for update in updates["result"]:
            try:
                update_id = update["update_id"]
                chat_id = update["message"]["chat"]["id"]
                mensage = update["message"]["text"]
                print(chat_id)
            except Exception as e:
                print(e)
            send_message(chat_id, "receba")
            last_update_id = update_id + 1
            time.sleep(2)


if __name__ == "__main__":
    # print(get_updates())
    # send_message(1345320802, "receba filha da truta")
    main()
