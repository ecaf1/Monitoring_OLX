import time
from urllib import response

import requests
from bs4 import BeautifulSoup

olx_url = "https://www.olx.com.br/brasil?q=caloi+estrada&sf=1&opst=2"

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
    print(novos_anuncios)
    main()
