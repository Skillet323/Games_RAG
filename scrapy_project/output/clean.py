import json
import re
from html import unescape

def clean_text(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"#+\s*", "", text)                # заголовки
    text = re.sub(r"\[\[.*?\]\]", "", text)          # вики-ссылки
    text = re.sub(r"\{\{.*?\}\}", "", text)          # шаблоны
    text = re.sub(r"\*\*|__|\*", "", text)           # жирный, курсив
    text = re.sub(r"\n+", "\n", text)                # лишние переводы строк
    text = re.sub(r"\s{2,}", " ", text)              # лишние пробелы
    return text.strip()

def clean_jsonl(input_path, output_path, min_text_length=100, excluded_titles=None):
    if excluded_titles is None:
        excluded_titles = {"Main Page", "Index", "Stub", "Stubs", "FAQ", "Navigation"}

    seen_titles = set()
    cleaned = []

    with open(input_path, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                entry = json.loads(line)

                title = entry.get("title", "").strip()
                raw_text = entry.get("full_text", "").strip()
                if not title or not raw_text:
                    continue

                cleaned_text = clean_text(raw_text)
                if len(cleaned_text) < min_text_length:
                    continue
                if title in excluded_titles:
                    continue
                if title in seen_titles:
                    continue

                entry["full_text"] = cleaned_text
                seen_titles.add(title)
                cleaned.append(entry)

            except json.JSONDecodeError:
                continue

    with open(output_path, "w", encoding="utf-8") as outfile:
        for entry in cleaned:
            json.dump(entry, outfile, ensure_ascii=False)
            outfile.write("\n")

    print(f"Очищено: {len(cleaned)} записей сохранено в {output_path}")

if __name__ == "__main__":
    clean_jsonl(
        input_path="combined.jl",
        output_path="combined_clean.jl"
    )
