import os
import re

import requests
from icalendar import Calendar

SOURCE_URL = os.environ["ICS_SOURCE_URL"]


def fetch_source() -> bytes:
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.raise_for_status()
    return resp.content


def classify(summary: str) -> str:
    """Decide which bucket an event belongs in based on its title."""
    s = (summary or "").upper()

    if "SELF-DIRECTED LEARNING" in s:
        return "self_directed"
    if re.search(r"\bC1\b", s):
        return "mandatory"
    return "other"


def new_calendar() -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//calendar-splitter//github-actions//")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    return cal


def main() -> None:
    raw = fetch_source()
    source_cal = Calendar.from_ical(raw)

    buckets = {
        "mandatory": new_calendar(),
        "self_directed": new_calendar(),
        "other": new_calendar(),
    }

    counts = {"mandatory": 0, "self_directed": 0, "other": 0}

    for component in source_cal.walk():
        if component.name != "VEVENT":
            continue
        summary = str(component.get("summary", ""))
        bucket = classify(summary)
        buckets[bucket].add_component(component)
        counts[bucket] += 1

    os.makedirs("output", exist_ok=True)
    for name, cal in buckets.items():
        path = f"output/{name}.ics"
        with open(path, "wb") as f:
            f.write(cal.to_ical())
        print(f"Wrote {path} ({counts[name]} events)")


if __name__ == "__main__":
    main()
