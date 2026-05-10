from pathlib import Path
import pandas as pd
import bibtexparser

INPUT = Path("data/library_all.bib")
CSV_OUT = Path("data/library_all.csv")
JSON_OUT = Path("data/library_all.json")

def clean_text(value):
    if not isinstance(value, str):
        return ""
    value = value.replace("{", "").replace("}", "")
    value = value.replace("\n", " ")
    value = value.replace(" and ", ", ")
    return " ".join(value.split())

with INPUT.open("r", encoding="utf-8") as f:
    bib_database = bibtexparser.load(f)

rows = []

for entry in bib_database.entries:
    rows.append({
        "id": entry.get("ID", ""),
        "type": entry.get("ENTRYTYPE", ""),
        "title": clean_text(entry.get("title", "")),
        "authors": clean_text(entry.get("author", "")),
        "year": clean_text(entry.get("year", "")),
        "journal": clean_text(entry.get("journal", "")),
        "booktitle": clean_text(entry.get("booktitle", "")),
        "doi": clean_text(entry.get("doi", "")),
        "url": clean_text(entry.get("url", "")),
        "keywords": clean_text(entry.get("keywords", "")),
        "abstract": clean_text(entry.get("abstract", "")),
    })

df = pd.DataFrame(rows)

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(CSV_OUT, index=False, encoding="utf-8")
df.to_json(JSON_OUT, orient="records", force_ascii=False, indent=2)

print(f"Created {CSV_OUT}")
print(f"Created {JSON_OUT}")
