import os
import json
import re
import unidecode

# Twoje frazy podejrzane
podejrzane_frazy = [
    "catering", "foodtruck", "obsługę imprez", "eventów", "gastronomiczn"
]

# Funkcja czyszcząca nazwę do zapisu pliku
def safe_filename(name):
    name = unidecode.unidecode(name)  # usuwamy polskie znaki
    name = re.sub(r'[<>:"/\\|?*]', '', name)  # zakazane znaki w Windows
    name = name.strip().replace(" ", "_")
    return name[:100]  # limit długości

# Wczytanie danych
with open("kpo.json", encoding="utf-8") as f:
    dane = json.load(f)

# Folder główny
base_dir = "podejrzane_rekordy"
os.makedirs(base_dir, exist_ok=True)

# Słownik do index.json
frazy_index = {fraza: [] for fraza in podejrzane_frazy}

# Przetwarzanie rekordów
for rekord in dane:
    opis = " ".join(str(v) for v in rekord.values() if v)
    for fraza in podejrzane_frazy:
        if fraza.lower() in opis.lower():
            folder_frazy = os.path.join(base_dir, safe_filename(fraza))
            os.makedirs(folder_frazy, exist_ok=True)

            nazwa_pliku = f"{rekord.get('Nazwa', rekord.get('name', 'rekord'))}.json"
            nazwa_pliku = safe_filename(nazwa_pliku)
            sciezka = os.path.join(folder_frazy, nazwa_pliku)

            with open(sciezka, "w", encoding="utf-8") as f:
                json.dump(rekord, f, ensure_ascii=False, indent=4)

            frazy_index[fraza].append(nazwa_pliku)

# Tworzenie plików index.json
for fraza, pliki in frazy_index.items():
    folder_frazy = os.path.join(base_dir, safe_filename(fraza))
    if pliki:  # jeśli są jakieś rekordy
        with open(os.path.join(folder_frazy, "index.json"), "w", encoding="utf-8") as f:
            json.dump(pliki, f, ensure_ascii=False, indent=4)

print("✅ Katalogowanie zakończone.")
