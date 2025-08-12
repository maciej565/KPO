import json
from rapidfuzz import fuzz
import re

# Parametry wyszukiwania
SZUKANE_SLOWO = "dywersyfikacja"
PROG_PODOBIENSTWA = 80  # 0-100 (im wyżej, tym mniej literówek zaakceptuje)

# Wczytanie pliku kpo.json
with open("kpo.json", "r", encoding="utf-8") as f:
    dane = json.load(f)

wyniki = []

for rekord in dane:
    for wartosc in rekord.values():
        if wartosc is None:
            continue
        tekst = str(wartosc).lower()
        # Sprawdzenie podobieństwa
        if fuzz.partial_ratio(SZUKANE_SLOWO, tekst) >= PROG_PODOBIENSTWA:
            wyniki.append(rekord)
            break  # Ten rekord już pasuje, nie trzeba sprawdzać dalej

# Zapis wyników do dywersyfikacja.json
with open("dywersyfikacja.json", "w", encoding="utf-8") as f:
    json.dump(wyniki, f, ensure_ascii=False, indent=4)

print(f"Zapisano {len(wyniki)} rekordów do dywersyfikacja.json")
