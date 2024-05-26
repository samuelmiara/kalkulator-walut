import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import os


def pobierz_kursy_walut():
    """funkcja pobiera kursy walut
    input brak
    output tabela kursow waluut w porownaniu do zlotowki"""
    try:
        response = requests.get('https://www.nbp.pl/kursy/xml/lasta.xml')
        response.raise_for_status()
        tabela_kursow = response.content
        with open('tabela_kursow.xml', 'wb') as file:
            file.write(tabela_kursow)
    except requests.exceptions.RequestException:
        if os.path.exists('tabela_kursow.xml'):
            with open('tabela_kursow.xml', 'rb') as file:
                tabela_kursow = file.read()
        else:
            tabela_kursow = None
    return tabela_kursow


def tab_kur(tabela_kursow):
    """funkcja przetwarza dane i zapisuje kursy walut
    input tabela_kursow
    output slownik kursy z zapisanymi kursami walut"""
    kursy = {}
    soup = BeautifulSoup(tabela_kursow, 'html.parser')
    waluty = soup.find_all('pozycja')
    kursy['PLN'] = {'nazwa': 'Polski złoty', 'kurs': 1.0}
    for waluta in waluty:
        kod = waluta.kod_waluty.text
        nazwa = waluta.nazwa_waluty.text
        kurs = float(waluta.kurs_sredni.text.replace(',', '.'))
        kursy[kod] = {'nazwa': nazwa, 'kurs': kurs}
    return kursy


def przelicz_waluty():
    """funkjca oblicza stosunek jednej waluty do drugiej
    input brak
    output wyswietla wynik jako tekst label_wynik """
    waluta_zrodlowa = combobox_zrodlowa.get().split(' - ')[0]
    waluta_docelowa = combobox_docelowa.get().split(' - ')[0]
    kwota_zrodlowa = float(entry_kwota.get())

    if waluta_zrodlowa == waluta_docelowa:
        wynik = kwota_zrodlowa
    else:
        if waluta_zrodlowa in kursy_walut and waluta_docelowa in kursy_walut:
            kurs_zrodlowy = kursy_walut[waluta_zrodlowa]['kurs']
            kurs_docelowy = kursy_walut[waluta_docelowa]['kurs']
            wynik = (kurs_zrodlowy /kurs_docelowy ) * kwota_zrodlowa
        else:
            wynik = "Błąd: Brak danych dotyczących wybranej waluty."

    label_wynik.configure(text=str(wynik))



window = tk.Tk()
window.title("Przelicznik walut")


tabela_kursow = pobierz_kursy_walut()
if tabela_kursow is not None:
    kursy_walut = tab_kur(tabela_kursow)
else:
    kursy_walut = {}


label_zrodlowa = tk.Label(window, text="Waluta źródłowa:")
label_zrodlowa.pack()
combobox_zrodlowa = ttk.Combobox(window,
                                 values=[f"{kod} - {kursy_walut[kod]['nazwa']}" for kod in kursy_walut])
combobox_zrodlowa.insert(tk.END, "PLN - Polski złoty")
combobox_zrodlowa.pack()

label_docelowa = tk.Label(window, text="Waluta docelowa:")
label_docelowa.pack()
combobox_docelowa = ttk.Combobox(window,
                                 values=[f"{kod} - {kursy_walut[kod]['nazwa']}" for kod in kursy_walut])
combobox_docelowa.insert(tk.END, "PLN - Polski złoty")
combobox_docelowa.pack()

label_kwota = tk.Label(window, text="Kwota:")
label_kwota.pack()
entry_kwota = tk.Entry(window)
entry_kwota.pack()

button_przelicz = tk.Button(window, text="Przelicz", command=przelicz_waluty)
button_przelicz.pack()

label_wynik = tk.Label(window, text="")
label_wynik.pack()

button_zakoncz = tk.Button(window, text="Zakończ", command=window.quit)
button_zakoncz.pack()

window.mainloop()
