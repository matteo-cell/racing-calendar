"""
Genera un file ICS per il calendario F1 usando l'API Jolpica
(successore gratuito e open source di Ergast).

Documentazione API: https://api.jolpi.ca/ergast/
"""

import sys
import requests
from datetime import datetime, timezone
from icalendar import Calendar, Event
from pathlib import Path

API_BASE = "https://api.jolpi.ca/ergast/f1"
OUTPUT_PATH = Path(__file__).parent.parent / "docs" / "f1.ics"

# Sessioni che vogliamo includere, in ordine di apparizione nel JSON Jolpica
SESSION_KEYS = [
    ("FirstPractice", "Prove Libere 1"),
    ("SecondPractice", "Prove Libere 2"),
    ("ThirdPractice", "Prove Libere 3"),
    ("Sprint", "Sprint"),
    ("SprintQualifying", "Sprint Qualifying"),
    ("Qualifying", "Qualifiche"),
]


def fetch_season(year: int) -> list[dict]:
    """Scarica il calendario completo della stagione da Jolpica."""
    url = f"{API_BASE}/{year}.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["MRData"]["RaceTable"]["Races"]


def make_event(summary: str, date_str: str, time_str: str, location: str, uid_suffix: str) -> Event:
    """Crea un evento ICS con orario UTC preciso (Jolpica fornisce sempre UTC con 'Z')."""
    dt_str = f"{date_str}T{time_str}"
    # Jolpica restituisce orari tipo "13:00:00Z" -> parse esplicito in UTC
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    event = Event()
    event.add("summary", summary)
    event.add("dtstart", dt)
    event.add("dtend", dt)  # evento puntuale; se vuoi una durata, sostituisci con dt + timedelta
    event.add("location", location)
    event.add("uid", f"f1-{uid_suffix}@racing-calendar")
    event.add("dtstamp", datetime.now(timezone.utc))
    return event


def build_calendar(races: list[dict]) -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//Racing Calendar//F1//IT")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", "F1 Calendar")
    cal.add("x-wr-timezone", "UTC")

    for race in races:
        race_name = race["raceName"]
        circuit = race["Circuit"]["circuitName"]
        round_num = race["round"]

        # Sessione gara principale
        if "date" in race and "time" in race:
            cal.add_component(
                make_event(f"{race_name} - Gara", race["date"], race["time"], circuit, f"race-{round_num}")
            )

        # Sessioni satellite (prove libere, qualifiche, sprint) se presenti
        for key, label in SESSION_KEYS:
            session = race.get(key)
            if session and "date" in session and "time" in session:
                cal.add_component(
                    make_event(
                        f"{race_name} - {label}",
                        session["date"],
                        session["time"],
                        circuit,
                        f"{key.lower()}-{round_num}",
                    )
                )

    return cal


def main():
    year = datetime.now().year
    print(f"Scarico calendario F1 {year}...")
    races = fetch_season(year)
    print(f"Trovate {len(races)} gare.")

    cal = build_calendar(races)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(cal.to_ical())

    print(f"File scritto in: {OUTPUT_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)
