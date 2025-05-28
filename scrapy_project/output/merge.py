def merge_jsonl_files(input_paths, output_path):
    with open(output_path, "w", encoding="utf-8") as outfile:
        for path in input_paths:
            with open(path, "r", encoding="utf-8") as infile:
                for line in infile:
                    outfile.write(line)
    print(f"Файл сохранён: {output_path}")


if __name__ == "__main__":
    merge_jsonl_files(
        ["Celeste_Pages_4.jl", "celeste_pages2.jl", "celeste_pages.jl"],
        "combined.jl"
    )
