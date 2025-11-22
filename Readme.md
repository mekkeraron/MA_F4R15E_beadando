Élő időjárási adatok lekérdezése


Hallgató: Mekker Áron
Neptunkód: F4R15E
Monogram: MA (a programban)


Feladat leírása:
A program egy tkinter alapú grafikus felületet biztosít, melynek segítségével a felhasználó a világ bármely településére rákereshet és lekérhet onnan valós, élő időjárási adatokat (égkép, hőmérséklet (°C és °F), páratartalom) az Open-Meteo API szolgáltatás használatával. A lekért adatokat élőben módosíthatja (azaz más város is lekérhető a futás közben), azokat elmentheti egy pillanatnyi_idojaras_adat.txt nevű szövegfájlba, valamint a korábban lekérdezett adatokat visszamenőleg megtekintheti a lekerdezesek.db adatbázisából.

A grafikus felületen található gombok és funkcióik:
- Adatok lekérése: A helységnév megadása után használható, lekérdezi és kijelzi a felületen az adatokat.
- Lekért adat mentése text fájlba: Az éppen képernyőn lévő adatokat összegzi és menti külső szövegfájlba. A mentés helyéről a felhasználó dönt.
- Előző lekérések: A korábban lekérdezett adatok egy adatbázisban tárolódnak. A szóban forgó adatbázis tartalmát lehet megtekinteni a gomb segítségével. Fontos: a program bezárása után az előzmények megmaradnak.
- Bezárás: Kilépés a programból.


Modulok és a modulokban használt függvények:
main.py
- A program belépési pontja
- Kialakítja a futási ablakot és elindítja az MAApp osztályt.

MA_idojaras.py
- Megtalálható benne a megjelenítéshez szükséges programkód és a saját osztály.
- Osztály: MAApp
- Függvények: 
  - idojaras_lekerdezes(self): az adatok lekérdezéséért és megjelenítéséért felel.
  - mentes_fajlba(self): külső szövegfájl készítését és mentését végzi el.
  - korabbi_lekeresek(self): új ablakban listázza a lekerdezesek.db adatbázist.

utils.py
- API lekérdezést, konvertálást, adatbázis szerkesztő műveleteket és a gifek megjelenítéséhez szükséges meghatározásokat tartalmaz. Fontos megjegyzés: amennyiben nem jelenik meg a gif a programban, célszerű ellenőrizni, hogy azok valóban a gyökérkonyvtárban vannak-e, valamint megfelelő fájlnévvel vannak ellátva (napos.gif, felhos.gif, stb...)
- Függvények:
  - elo_ido_lekerdezes(): az élő adatokat kérdezi le.
  - kod_egkep_meghatarozas(): Az API kódjait felelteti meg az adott égképekkel.
  - MA_fahrenheit_konvertalas(): Celsius fokot vált át Fahrenheitbe.
  - adatszoveg_forma(): a szöveges fájl szövegstílusa itt kerül megszabásra.
  - db_init(): lekerdezesek.db nevű adatbázist készít a program gyökerébe, ha az még nem létezik.
  - db_insert(): a jelenlegi lekérdezést illeszti be a lekerdezesek.db adatbázisba.
  - db_fetch_all(): listázza az előző 100 lekérdezést a lekerdezesek.db-ben.


Saját elemek:
- függvény: MA_fahrenheit_konvertalas()
- osztály: MAApp
- modul: MA_idojaras.py

Használt modulok:
- Tanult modul: tkinter, sqlite3, requests
- Bemutatandó (keresett) modul: datetime, os
- Saját modul: MA_idojaras.py

A program indításához esetlegesen telepíteni szükséges függőség:
pip install requests

A program futásához társuló fájlok listája (szükséges helyük: gyökérkönyvtár):
- napos.gif
- felhos.gif
- esos.gif
- havas.gif
- zivatar.gif
- szeles.gif
- ismeretlen.gif
