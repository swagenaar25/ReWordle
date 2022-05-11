with open("unprocessed_latin.txt", encoding="utf-8") as in_file:
    with open("processed_latin_1.txt", "w", encoding="utf-8") as out_file:
        for line in in_file:
            if not (line[0] in "'&-+0123456789=") and line[0].lower() == line[0] and " " not in line and "-" not in line and "." not in line:
                out_file.write(line)
