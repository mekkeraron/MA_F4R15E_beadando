import requests
import sqlite3
import os



def elo_ido_lekerdezes(city_name):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        geo_response = requests.get(geo_url, timeout=10)
        if geo_response.status_code != 200:
            return None
        geo_data = geo_response.json()
        if "results" not in geo_data or not geo_data["results"]:
            return None
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m&timezone=auto"
        w_response = requests.get(weather_url, timeout=10)
        if w_response.status_code != 200:
            return None
        w_data = w_response.json()
        if "current_weather" not in w_data:
            return None
        current = w_data["current_weather"]
        celsius = current.get("temperature", 0)
        windspeed = current.get("windspeed", 0)
        weathercode = current.get("weathercode", 0)
        humidity = 0
        hourly = w_data.get("hourly", {})
        times = hourly.get("time", [])
        hums = hourly.get("relativehumidity_2m", [])
        try:
            idx = times.index(current.get("time"))
            humidity = hums[idx] if idx < len(hums) else 0
        except Exception:
            humidity = 0
        description = kod_egkep_meghatarozas(weathercode)
        if windspeed and windspeed >= 15:
            description = "Szeles"
        return {"temperature": celsius, "description": description, "humidity": humidity, "windspeed": windspeed}
    except Exception:
        return None




def kod_egkep_meghatarozas(code):
    if code in (0, 1):
        return "Derült"
    if code in (2, 3, 45, 48):
        return "Borult"
    if code in range(51, 68) or code in (80, 81, 82):
        return "Eső"
    if code in range(71, 78) or code in (85, 86):
        return "Havazás"
    if code in range(95, 100):
        return "Zivatar"
    return "Nincs adat"




def MA_fahrenheit_konvertalas(celsius):
    return round(celsius * 9 / 5 + 32, 1)




def adatszoveg_forma(varos, datum, celsius, fahrenheit, paratart, egkep):
    return (f"{varos}\n{datum}\n"
            f"Hőmérséklet: {celsius} °C / {fahrenheit} °F\n"
            f"Páratartalom: {paratart}%\n"
            f"Égkép: {egkep}")





def db_init(db_path="lekerdezesek.db"):
    exists = os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS lekerdezesek (varos TEXT, datum TEXT, celsius REAL, paratart INT, egkep TEXT)")
    conn.commit()
    conn.close()

def db_insert(entry, db_path="lekerdezesek.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO lekerdezesek (varos, datum, celsius, paratart, egkep) VALUES (?, ?, ?, ?, ?)",
                (entry["varos"], entry["datum"], entry["celsius"], entry["paratart"], entry["egkep"]))
    conn.commit()
    conn.close()

def db_fetch_all(db_path="lekerdezesek.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT varos, datum, celsius, paratart, egkep FROM lekerdezesek ORDER BY rowid DESC LIMIT 100")
    rows = cur.fetchall()
    conn.close()
    return rows
