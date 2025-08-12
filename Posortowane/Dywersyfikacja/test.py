import json
import tkinter as tk
from tkinter import filedialog, messagebox

def polacz_jsony():
    # Wybór wielu plików JSON
    pliki = filedialog.askopenfilenames(
        title="Wybierz pliki JSON",
        filetypes=[("Pliki JSON", "*.json")]
    )
    
    if not pliki:
        return
    
    polaczone_dane = []
    
    for plik in pliki:
        try:
            with open(plik, "r", encoding="utf-8") as f:
                dane = json.load(f)
                # Jeśli JSON jest listą, dodaj elementy
                if isinstance(dane, list):
                    polaczone_dane.extend(dane)
                else:
                    # Jeśli to obiekt (dict), dodaj jako element listy
                    polaczone_dane.append(dane)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się odczytać {plik}: {e}")
            return
    
    # Zapis do nowego pliku
    plik_wyj = filedialog.asksaveasfilename(
        title="Zapisz połączony JSON",
        defaultextension=".json",
        filetypes=[("Pliki JSON", "*.json")]
    )
    
    if not plik_wyj:
        return
    
    try:
        with open(plik_wyj, "w", encoding="utf-8") as f:
            json.dump(polaczone_dane, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Sukces", "Pliki JSON zostały połączone i zapisane!")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {e}")

# Tworzenie prostego GUI
root = tk.Tk()
root.title("Łączenie plików JSON")

btn = tk.Button(root, text="Połącz pliki JSON", command=polacz_jsony)
btn.pack(padx=20, pady=20)

root.mainloop()
