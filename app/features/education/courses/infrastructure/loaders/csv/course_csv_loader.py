import csv
import re


class CourseCSVLoader:

    @staticmethod
    def parse(raw: str):
        match = re.match(r"^(.*?)\s*\((.*?)\)$", raw.strip())
        if match:
            return match.group(1), match.group(2)
        return raw.strip(), None

    @staticmethod
    def load(path: str):
        encodings = ["utf-8", "latin-1", "cp1252"]

        for enc in encodings:
            try:
                with open(path, newline="", encoding=enc) as file:
                    return list(csv.DictReader(file))
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
                        name, acronym = CourseCSVLoader.parse(row["Nombre del Curso"])

                        try:
                            await use_case.execute(name, acronym)
                        except ValueError:
                            pass
                    return

            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError("Could not decode CSV with tried encodings.")
