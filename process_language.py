bad = "1234567890"
lowercase = "abcdefghijklmnopqrstuvwxyz\n"
replacement = {
    "ö": "o",
    "è": "e",
    "ë": "e",
    "ï": "i",
    "ü": "u",
    "é": "e",
    "ê": "e",
    "å": "a",
    "û": "u",
    "ç": "c"
}
with open("dutch_raw.txt", encoding="utf-8") as in_file:
    with open("assets/lang/nl.txt", "w", encoding="utf-8") as out_file:
        for line in in_file:
            if not (line[0] in "'&-+0123456789=") and line[0].lower() == line[0] and " " not in line and "-" not in line and "." not in line:
                ok = True
                for letter in line:
                    if letter in bad:
                        ok = False
                        break
                if ok:
                    for k in replacement:
                        v = replacement[k]
                        line = line.replace(k, v)
                    ok = True
                    for letter in line:
                        if letter not in lowercase:
                            ok = False
                            if "'" not in line and "ó" not in line:
                                print(f"Rejected: [{line}]")
                            break
                    if ok:
                        out_file.write(line)
