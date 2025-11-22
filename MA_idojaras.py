import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from utils import elo_ido_lekerdezes, adatszoveg_forma, MA_fahrenheit_konvertalas, db_init, db_insert, db_fetch_all



class MAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("app")
        self.root.geometry("580x300")
        db_init()
        self.jelenlegi_adat = None

        self.gifek = {}
        for key, fname in (
            ("Derült", "napos.gif"),
            ("Borult", "felhos.gif"),
            ("Eső", "esos.gif"),
            ("Havazás", "havas.gif"),
            ("Zivatar", "zivatar.gif"),
            ("Szeles", "szeles.gif"),
            ("Nincs adat", "ismeretlen.gif"),
        ):
            try:
                self.gifek[key] = tk.PhotoImage(file=fname)
            except Exception:
                self.gifek[key] = None

        main_frame = ttk.Frame(root, padding=8)
        main_frame.pack(fill="both")

        for i in range(3):
            main_frame.columnconfigure(i, weight=1, uniform="col")
        for i in range(4):
            main_frame.rowconfigure(i, weight=1, uniform="row")

        self.varos_cim = ttk.Label(main_frame, text="Város megadása:", font=("Arial", 11))
        self.varos_cim.grid(row=0, column=0, sticky="e", padx=(5, 2), pady=(5, 2))
        self.varos_textbox = ttk.Entry(main_frame, width=22, font=("Arial", 11))
        self.varos_textbox.grid(row=0, column=1, columnspan=2, sticky="w", padx=(2, 5), pady=(5, 2))

        table = ttk.Frame(main_frame)
        table.grid(row=1, column=0, columnspan=3, rowspan=3, sticky="nsew", pady=5)
        for i in range(3):
            table.columnconfigure(i, weight=1, uniform="tabcol")
            table.rowconfigure(i, weight=1, uniform="tabrow")


        self.lekerdezett_varos = ttk.Label(table, text="", font=("Arial", 12, "bold"), anchor="center")
        self.lekerdezett_varos.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)

        right_cell = ttk.Frame(table)
        right_cell.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)
        right_cell.columnconfigure(0, weight=1)
        right_cell.rowconfigure(0, weight=1)
        self.gif_rajz = ttk.Label(right_cell, anchor="center")
        self.gif_rajz.grid(row=0, column=0)
        self.homerseklet_egkep = ttk.Label(right_cell, text="", font=("Arial", 10), anchor="center", justify="center")
        self.homerseklet_egkep.grid(row=1, column=0)

        self.datum = ttk.Label(table, text="", font=("Arial", 10), anchor="center")
        self.datum.grid(row=0, column=2, sticky="nsew", padx=3, pady=3)


        self.lekeres_gomb = ttk.Button(table, text="Adatok lekérése", command=self.idojaras_lekerdezes)
        self.lekeres_gomb.grid(row=1, column=0, padx=3, pady=3)

        self.mentes_fajlba_gomb = ttk.Button(table, text="Lekért adat mentése text fájlba...", command=self.mentes_fajlba)
        self.mentes_fajlba_gomb.grid(row=1, column=1, padx=3, pady=3)

        self.elozmeny_gomb = ttk.Button(table, text="Előző lekérések", command=self.korabbi_lekeresek)
        self.elozmeny_gomb.grid(row=1, column=2, padx=3, pady=3)


        self.kilepes_gomb = ttk.Button(table, text="Bezárás", width=28, command=self.root.destroy)
        self.kilepes_gomb.grid(row=2, column=0, columnspan=3, padx=5)




    def idojaras_lekerdezes(self):
        varos = self.varos_textbox.get().strip()
        if not varos:
            messagebox.showwarning("Hiányzó adat", "Élő adat lekérdezéséhez előbb meg kell adni a keresett helység nevét!")
            return
        data = elo_ido_lekerdezes(varos)
        if data:
            celsius = data["temperature"]
            fahrenheit = MA_fahrenheit_konvertalas(celsius)
            egkep = data["description"]
            paratart = data.get("humidity", 0)
            datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.lekerdezett_varos.config(text=varos.title())
            self.datum.config(text=datum)
            self.homerseklet_egkep.config(text=f"{egkep}\n{celsius} °C / {fahrenheit} °F")
            self.jelenlegi_adat = {"varos": varos, "datum": datum, "celsius": celsius, "fahrenheit": fahrenheit, "paratart": paratart, "egkep": egkep}
            db_insert(self.jelenlegi_adat)
            icon = self.gifek.get(egkep)
            if icon:
                self.gif_rajz.config(image=icon, text="")
                self.gif_rajz.image = icon
            else:
                self.gif_rajz.config(image="", text=egkep)
        else:
            messagebox.showerror("Lekérdezési hiba", "Nem áll rendelkezésre élő adat a megadott településhez.")




    def mentes_fajlba(self):
        if not self.jelenlegi_adat:
            messagebox.showwarning("Nincs érvényes pillanatnyi lekérdezés", "Élő adat mentéséhez először meg kell adni a lekérdezni kívánt település nevét, majd a lekérés gombra kell kattintani!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Szöveges fájl", "*.txt")], initialfile="pillanatnyi_idojaras_adat.txt")
        if not file_path:
            return
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(adatszoveg_forma(self.jelenlegi_adat["varos"], self.jelenlegi_adat["datum"], self.jelenlegi_adat["celsius"], self.jelenlegi_adat["fahrenheit"], self.jelenlegi_adat["paratart"], self.jelenlegi_adat["egkep"]))
        messagebox.showinfo("Sikeres mentés", "A megjelenített adatok mentésre kerültek!")




    def korabbi_lekeresek(self):
        rows = db_fetch_all()
        win = tk.Toplevel(self.root)
        win.title("Korábbi lekérések")
        win.geometry("525x290")
        text = tk.Text(win, wrap="word")
        text.pack(expand=True, fill="both")
        if not rows:
            text.insert("end", "Nincs tárolva korábbi lekérdezés.")
            return
        for r in rows:
            varos, date, temp, paratart, egkep = r
            fahrenheit = MA_fahrenheit_konvertalas(temp)
            entry = adatszoveg_forma(varos, date, temp, fahrenheit, paratart, egkep)
            text.insert("end", entry + "\n\n")
