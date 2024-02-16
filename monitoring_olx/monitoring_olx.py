import json
import time

import requests  # cloudscrap
from bs4 import BeautifulSoup

olx_url = "https://www.olx.com.br/brasil"

novos_anuncios = set()
intervalo_verificacao = 3600


def obter_links_anuncios(url):
    links = set()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    anuncios = soup.find_all("a", {"class": "olx-ad-card__link-wrapper"})
    for anuncio in anuncios:
        link = anuncio.get("href")
        if link:
            links.add(link)
    print(len(links))
    return links


def verificar_novos_anuncios():
    global novos_anuncios
    print("Verificando novos anuncio...")
    links_anuncios = obter_links_anuncios(olx_url)
    novos = links_anuncios - novos_anuncios
    if novos:
        for link in novos:
            print(f"Novos anúncios encontrado: {link}")
        novos_anuncios.update(novos)
    else:
        print("Nenhum novo anuncio encontrado.")


def main():
    while True:
        verificar_novos_anuncios()
        time.sleep(intervalo_verificacao)


if __name__ == "__main__":
    # print(novos_anuncios)
    # main()
    sessao = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    payload = {"q": "caloi%20estradacle"}
    response = sessao.get(olx_url, headers=headers)
    print(response.request.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    resu = soup.find(id="__NEXT_DATA__")
    with open("resu.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    data = json.loads(getattr(resu, "text"))
    with open("resu.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
