import json
import os
import re
import hashlib

def safe_filename(value, max_len=20):
    if value is None:
        return "None"
    value = str(value).strip()
    # Usuń znaki kontrolne (newline, tab, carriage return)
    value = re.sub(r'[\r\n\t]+', ' ', value)
    # Zamień znaki niedozwolone na _
    value = re.sub(r'[\\/*?:"<>|]', "_", value)
    # Zamień spacje na _
    value = value.replace(" ", "_")
    # Skróć i dodaj hash jeśli nazwa jest za długa
    if len(value) > max_len:
        h = hashlib.sha256(value.encode('utf-8')).hexdigest()[:8]
        value = value[:max_len] + "_" + h
    return value or "empty"

# Wczytanie danych z pliku dane.json
with open("kpo.json", "r", encoding="utf-8") as f:
    dane = json.load(f)

# Pola, po których chcesz segregować rekordy
pola = [
    "name", "address", "description", "styleUrl", "opis", "adres",
    "Województwo", "Powiat", "Miejscowość", "Kod pocztowy", "Ulica", "Numer"
]

for pole in pola:
    folder = pole
    os.makedirs(folder, exist_ok=True)

    # Grupowanie rekordów po wartości pola
    grupy = {}
    for rekord in dane:
        wartosc = rekord.get(pole, None)
        grupy.setdefault(wartosc, []).append(rekord)

    # Zapis do osobnych plików JSON
    for wartosc, rekordy in grupy.items():
        nazwa_pliku = safe_filename(wartosc) + ".json"
        sciezka = os.path.join(folder, nazwa_pliku)
        with open(sciezka, "w", encoding="utf-8") as f:
            json.dump(rekordy, f, ensure_ascii=False, indent=2)

print("Rekordy zostały posegregowane i zapisane w osobnych folderach.")
