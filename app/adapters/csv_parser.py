import csv
import unicodedata
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from app.core.entities.course import Course
from app.core.ports.parser import Parser

"""
CsvParser is a class that implements the Parser interface.

Attributes:
    HEADER_MAPS: A dictionary that maps the header names to the actual column names.
    SEP_CANDIDATES: A list of possible separators for the CSV file.

Methods:
    _normalize_headers(headers: List[str]) -> dict: Normalizes the headers.
    _parse_prereq(value: str) -> List[str]: Parses the prerequisites.
    _coerce_int(value: str, default: int = 0) -> int: Coerces the value to an integer.
    _open_with_fallback(path: Path) -> Tuple[object, str]: Opens the file with fallback.
    _normalize_text(value: Optional[str]) -> str: Normalizes the text.
    load_courses(source_path: str, university: Optional[str] = None, career: Optional[str] = None, program: Optional[str] = None) -> Iterable[Course]: Loads the courses.
"""
class CsvParser(Parser):
    HEADER_MAPS = {
        "university": {"universidad", "university"},
        "career": {"carrera", "career", "major"},
        "program": {"programa", "program", "track"},
        "cycle": {"ciclo", "cycle", "semestre", "semester"},
        "name": {"nombre", "curso", "name", "course", "nombre del curso"},
        "code": {"codigo", "código", "code", "id"},
        "credits": {"creditos", "créditos", "credits", "credit"},
        "prerequisites": {
            "prerrequisitos",
            "prerequisitos",
            "prerreq",
            "prerequisites",
            "prereqs",
        },
    }

    SEP_CANDIDATES = [";", ",", "|", "/", "+", "-", " "]
    """
    _normalize_headers is a function that normalizes the headers.

    Args:
        headers (List[str]): The headers.

    Returns:
        dict: The normalized headers.
    """
    def _normalize_headers(self, headers: List[str]) -> dict:
        norm = {h.strip().lower(): i for i, h in enumerate(headers)}
        col_idx = {}
        for key, aliases in self.HEADER_MAPS.items():
            for a in aliases:
                if a in norm:
                    col_idx[key] = norm[a]
                    break
        return col_idx

    """
    _parse_prereq is a function that parses the prerequisites.

    Args:
        value (str): The value.

    Returns:
        List[str]: The parsed prerequisites.
    """
    def _parse_prereq(self, value: str) -> List[str]:
        if not value:
            return []
        raw = str(value).strip()
        for sep in self.SEP_CANDIDATES:
            if sep in raw:
                parts = [p.strip() for p in raw.split(sep)]
                return [p for p in parts if p]
        return [raw] if raw else []

    """
    _coerce_int is a function that coerces the value to an integer.

    Args:
        value (str): The value.
        default (int): The default value.

    Returns:
        int: The coerced value.
    """
    def _coerce_int(self, value: str, default: int = 0) -> int:
        try:
            return int(str(value).strip())
        except Exception:
            try:
                return int(float(str(value).strip().replace(",", ".")))
            except Exception:
                return default

    """
    _open_with_fallback is a function that opens a file with fallback.

    Args:
        path (Path): The path to the file.

    Returns:
        Tuple[object, str]: The file and sample.
    """
    def _open_with_fallback(self, path: Path) -> Tuple[object, str]:
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        last_err = None
        for enc in encodings:
            try:
                f = path.open("r", encoding=enc, newline="")
                try:
                    sample = f.read(4096)
                    f.seek(0)
                    return f, sample
                except UnicodeDecodeError as e:
                    last_err = e
                    f.close()
            except Exception as e:
                last_err = e
        raise last_err

    """
    _normalize_text is a function that normalizes the text.

    Args:
        value (Optional[str]): The value.

    Returns:
        str: The normalized text.
    """
    def _normalize_text(self, value: Optional[str]) -> str:
        if not value:
            return ""
        value = unicodedata.normalize("NFKD", value)
        value = "".join(ch for ch in value if not unicodedata.combining(ch))
        return " ".join(value.lower().strip().split())

    """
    load_courses is a function that loads the courses.

    Args:
        source_path (str): The path to the source file.
        university (Optional[str]): The university.
        career (Optional[str]): The career.
        program (Optional[str]): The program.

    Returns:
        Iterable[Course]: The courses.
    """
    def load_courses(
        self,
        source_path: str,
        university: Optional[str] = None,
        career: Optional[str] = None,
        program: Optional[str] = None,
    ) -> Iterable[Course]:
        path = Path(source_path)
        if not path.exists():
            raise FileNotFoundError(str(path))

        file_handle = None
        try:
            file_handle, sample = self._open_with_fallback(path)
            try:
                dialect = csv.Sniffer().sniff(sample)
            except Exception:
                dialect = csv.excel
            reader = csv.reader(file_handle, dialect)
            try:
                headers = next(reader)
            except StopIteration:
                return []
            col = self._normalize_headers(headers)

            filter_university = self._normalize_text(university)
            filter_career = self._normalize_text(career)
            filter_program = self._normalize_text(program)

            def get(row, key, default=""):
                idx = col.get(key)
                return row[idx].strip() if idx is not None and idx < len(row) else default

            filtered: List[Course] = []
            for row in reader:
                if not row or all(not c.strip() for c in row):
                    continue
                uni = get(row, "university")
                car = get(row, "career")
                prog = get(row, "program")
                uni_norm = self._normalize_text(uni)
                car_norm = self._normalize_text(car)
                prog_norm = self._normalize_text(prog)

                if filter_university and filter_university not in uni_norm:
                    continue
                if filter_career and filter_career not in car_norm:
                    continue
                if filter_program and filter_program not in prog_norm:
                    continue

                code = get(row, "code")
                name = get(row, "name")
                credits = self._coerce_int(get(row, "credits"), default=0)
                cycle = self._coerce_int(get(row, "cycle"), default=0)
                prereq = self._parse_prereq(get(row, "prerequisites"))

                if not code:
                    continue
                filtered.append(
                    Course(
                        code=code,
                        name=name or code,
                        credits=credits,
                        cycle=cycle,
                        university=uni or None,
                        career=car or None,
                        program=prog or None,
                        prerequisites=prereq,
                    )
                )
            return filtered
        finally:
            if file_handle:
                file_handle.close()
