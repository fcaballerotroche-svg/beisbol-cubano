import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://www.beisbolcubano.cu/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def extraer():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=25)
        res.raise_for_status()
    except Exception as e:
        print(f"Error conectando al sitio oficial: {e}")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    datos = {
        "juegos": [],
        "lideres": [],
        "logos": []
    }

    # 1. Extraer marcadores y partidos
    bloques = soup.find_all(["div", "section"], class_=re.compile(r"scoreboard|match|game", re.I))
    for b in bloques:
        t = b.get_text(separator=" ", strip=True)
        if t:
            datos["juegos"].append(t)

    # 2. Rutas completas de logos y fotos reales
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src:
            if not src.startswith("http"):
                src = f"https://www.beisbolcubano.cu{src}"
            datos["logos"].append({
                "alt": img.get("alt", ""),
                "url": src
            })

    # 3. Guardar en datos.json
    with open("datos.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    print("Archivo datos.json creado con exito.")

if __name__ == "__main__":
    extraer()
