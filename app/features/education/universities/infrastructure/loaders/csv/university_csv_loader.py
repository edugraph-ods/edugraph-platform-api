import csv
import re


class UniversityCSVLoader:

    @staticmethod
    def parse(raw: str):
        cleaned = raw.replace("\u00A0", " ").strip()
        match = re.match(r"^(.*?)\s*\((.*?)\)$", cleaned)
        if match:
            return match.group(1), match.group(2)
        name = cleaned
        acronym = UniversityCSVLoader.generate_acronym(name)
        if not acronym:
            parts = [p for p in re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]"," ", name).split() if p]
            acronym = "".join(w[0].upper() for w in parts[:4]) or "UNI"
        return name, acronym

    @staticmethod
    def generate_acronym(name: str) -> str:
        name_norm = re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]"," ", name.replace("\u00A0"," "))
        words_raw = (
            name_norm
                .replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U")
                .replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
        ).split()
        words_lower = [w.lower() for w in words_raw]
        if {"nacional","mayor","san","marcos"}.issubset(set(words_lower)):
            return "UNMSM"
        if {"catolica","santa","maria"}.issubset(set(words_lower)):
            return "USMP"
        if {"catolica","peruana"}.issubset(set(words_lower)):
            return "PUCP"
        if {"nacional","ingenieria"}.issubset(set(words_lower)):
            return "UNI"
        if "pacifico" in words_lower:
            return "UP"
        if "lima" in words_lower:
            return "UL"

        stop = {"de","la","las","los","del","y","en","el","universidad","peruana","nacional"}
        major = [w for w in words_raw if len(w) > 3 and w.lower() not in stop]
        if major:
            return "".join(w[0].upper() for w in major[:4])
        return "".join(w[0].upper() for w in words_raw[:4])

    @staticmethod
    def load(path: str):
        encodings = ["utf-8", "latin-1", "cp1252"]

        for enc in encodings:
            try:
                with open(path, newline="", encoding=enc) as file:
                    reader = csv.DictReader(file)
                    return list(reader)
            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError("Could not decode CSV with tried encodings.")

    @staticmethod
    async def load_and_insert(path, use_case):
        encodings = ["utf-8", "latin-1", "cp1252"]

        for enc in encodings:
            try:
                with open(path, newline="", encoding=enc) as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        name, acronym = UniversityCSVLoader.parse(row["Universidad "])

                        try:
                            await use_case.execute(name, acronym)
                        except ValueError:
                            pass
                    return

            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError("Could not decode CSV with tried encodings.")
