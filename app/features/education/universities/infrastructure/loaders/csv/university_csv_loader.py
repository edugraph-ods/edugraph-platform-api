import csv
import re


class UniversityCSVLoader:

    @staticmethod
    def parse(raw: str):
        match = re.match(r"^(.*?)\s*\((.*?)\)$", raw.strip())
        if match:
            name = match.group(1).strip()
            acronym = match.group(2).strip()
        else:
            name = raw.strip()
            acronym = UniversityCSVLoader.extract_acronym_from_name(name)

        if not acronym:
            acronym = ''.join([w[0].upper() for w in name.split() if w])
        return name, acronym

    @staticmethod
    def extract_acronym_from_name(name: str):
        words = name.split()
        if len(words) >= 2:
            return ''.join(w[0].upper() for w in words[:3])
        return name[:3].upper()

    @staticmethod
    def load(path: str):
        encodings = ["utf-8-sig", "latin-1", "cp1252"]

        for enc in encodings:
            try:
                with open(path, newline="", encoding=enc) as file:
                    reader = csv.DictReader(file)
                    print("HEADERS:", reader.fieldnames)
                    return list(reader)
            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError("Could not decode CSV with tried encodings.")

    @staticmethod
    async def load_and_insert(path, use_case):
        encodings = ["utf-8-sig", "latin-1", "cp1252"]

        for enc in encodings:
            try:
                with open(path, newline="", encoding=enc) as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        row = {k.replace('\ufeff', ''): v for k, v in row.items()}

                        name, acronym = UniversityCSVLoader.parse(row["Universidad"])

                        try:
                            await use_case.execute(name, acronym)
                        except ValueError:
                            pass
                return

            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError("Could not decode CSV with tried encodings.")
