import os
import time

import requests
from dotenv import load_dotenv

from monitoring_olx import get_ad_data  # type: ignore

load_dotenv()

# Acessa as variáveis de ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN", "")
URL = f"https://api.telegram.org/bot{TOKEN}/"
state_chat = {}
sesion = requests.Session()

AWAITING_COMMAND, AWAITING_PRODUCT, AWAITING_STATE = range(3)


def get_updates(last_update_id=None):
    url = URL + "getUpdates?timeout=100"
    if last_update_id:
        url += f"&offset={last_update_id}"
    response = sesion.get(url)
    return response.json()


def send_message(chat_id, text):
    url = URL + f"sendMessage?chat_id={chat_id}&text={text}"

    response = sesion.get(url)
    x = response.json()


def main():
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        for update in updates["result"]:
            try:
                update_id = update["update_id"]
                chat_id = update["message"]["chat"]["id"]
                mensage = update["message"]["text"]

                current_state = state_chat.get(chat_id, AWAITING_COMMAND)

                if current_state == AWAITING_COMMAND and mensage.lower() == "/olx":
                    state_chat[chat_id] = AWAITING_PRODUCT
                    send_message(chat_id, "envie o nome do produto")
                elif current_state == AWAITING_PRODUCT:
                    state_chat[chat_id] = AWAITING_STATE
                    current_state.get(chat_id)
                    send_message(chat_id, "Agora, envie a sigla do estado ou digite 'todo' para todo o Brasil.")
                elif current_state == AWAITING_STATE:
                    estado = mensage if mensage.lower() != 'todo' else None
                    state_chat[chat_id] = AWAITING_COMMAND
                    data_ad = get_ad_data()
            except Exception as e:
                print(e)
            send_message(chat_id, "receba")
            last_update_id = update_id + 1
            time.sleep(2)


if __name__ == "__main__":
    # print(get_updates())
    # send_message(1345320802, "receba filha da truta")
    main()
