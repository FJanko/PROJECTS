import requests

def posli_pozadavek_get(url):
    odpoved = requests.get(url)
    return odpoved.text

def ziskej_parsovanou_odpoved(odpoved_serveru):
    return BeautifulSoup(odpoved_serveru, "html.parser")

def vyber_tr_tagy(parsovana_odpoved):
    tabulka = parsovana_odpoved.find("table")
    if tabulka:
        return tabulka.find_all("tr")
    return []

def rozdel_zahlavi_a_transakce(vsechny_tr_tagy):
    if not vsechny_tr_tagy:
        return [], []

    zahlavi_tagy = vsechny_tr_tagy[0].find_all("th")
    prvni_hodnota = [th.get_text(strip=True) for th in zahlavi_tagy]

    druha_hodnota = vsechny_tr_tagy[1:]

    return prvni_hodnota, druha_hodnota


url_adresa = "https://ib.fio.cz/ib/transparent?a=2701783211&f=01.07.2023&t=03.07.2023"

hrube_html = posli_pozadavek_get(url_adresa)
naparsovana_data = ziskej_parsovanou_odpoved(hrube_html)
tagy_tr = vyber_tr_tagy(naparsovana_data)
jmena_poli, transakce = rozdel_zahlavi_a_transakce(tagy_tr)

print("Jména polí (Záhlaví):", jmena_poli)
print("-" * 50)

if transakce:
    print("Ukázka výstupu první transakce:\n")
    print(transakce[0].prettify())
else:
    print("Nebyly nalezeny žádné transakce.")