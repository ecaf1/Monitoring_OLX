import json
import time

import requests
from bs4 import BeautifulSoup

OLX_URL = "https://www.olx.com.br/"

novos_anuncios = set()
intervalo_verificacao = 3600

sesion = requests.Session()
sesion.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
)


def get_ad_data(produvt, stare_key="brasil/"):
    my_ads = []

    if stare_key != "brasil/":
        url = OLX_URL + f"estado-{stare_key.lower()}"
    else:
        url = OLX_URL + stare_key

    params = {"q": produvt}
    try:
        response = sesion.get(url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        ads_gloss = soup.find(id="__NEXT_DATA__")
        ad_json = json.loads(getattr(ads_gloss, "text"))
        ads = ad_json["props"]["pageProps"]["ads"]
        for ad in ads:
            ad_data = {
                "title": ad["title"],
                "price": ad["price"],
                "url_ad": ad["url"],
                "url_images": [image["original"] for image in ad["images"]],
            }
            my_ads.append(ad_data)
    except requests.HTTPError as e:
        print(e)
    return my_ads


def verificar_novos_anuncios(): ...


#     global novos_anuncios
#     print("Verificando novos anuncio...")
#     links_anuncios = obter_links_anuncios(OLX_URL)
#     novos = links_anuncios - novos_anuncios
#     if novos:
#         for link in novos:
#             print(f"Novos anúncios encontrado: {link}")
#         novos_anuncios.update(novos)
#     else:
#         print("Nenhum novo anuncio encontrado.")


def main():
    while True:
        verificar_novos_anuncios()
        time.sleep(intervalo_verificacao)


if __name__ == "__main__":
    # print(novos_anuncios)
    # main()
    # sessao = requests.Session()
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    # }
    # payload = {"q": "caloi%20estradacle"}
    # response = sessao.get(OLX_URL, headers=headers)
    # print(response.request.headers)
    # soup = BeautifulSoup(response.text, "html.parser")
    # resu = soup.find(id="__NEXT_DATA__")
    # with open("resu.html", "w", encoding="utf-8") as f:
    #     f.write(soup.prettify())
    # data = json.loads(getattr(resu, "text"))
    # with open("resu.json", "w") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
    print(get_ad_data("caloi strada", stare_key="AL"))
