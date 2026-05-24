from __future__ import annotations

import re
from typing import Dict, Iterable, List

import pandas as pd

from .utils import canonical_book_key, extract_isbn, short_hash

NON_BOOK_HINTS = [
    "manaba",
    "授業時",
    "授業中",
    "配付",
    "配布",
    "プリント",
    "資料を配",
    "webで公開",
    "url",
    "http://",
    "https://",
]


def split_reference_text(text: object) -> List[str]:
    if text is None:
        return []
    s = str(text).replace("\r\n", "\n").replace("\r", "\n")
    # Bullet markers and Japanese list separators often appear in KdB-style fields.
    s = re.sub(r"[\u2022●○■◆◇▶▷]\s*", "\n", s)
    parts: List[str] = []
    for line in s.split("\n"):
        line = re.sub(r"^\s*[-*・]\s*", "", line).strip()
        if not line:
            continue
        # Split very long semicolon-separated bibliographies conservatively.
        semis = re.split(r"(?<=\))\s*[;；]\s*|\s*[;；]\s*(?=(?:ISBN|[A-Z][A-Za-z]+,|[^\x00-\x7F]+『))", line)
        for item in semis:
            item = item.strip(" ・,，;；")
            if item:
                parts.append(item)
    return parts


def _extract_japanese_bracket_title(line: str) -> str:
    for left, right in [("『", "』"), ("「", "」"), ("《", "》")]:
        m = re.search(re.escape(left) + r"([^" + re.escape(right) + r"]{2,})" + re.escape(right), line)
        if m:
            return m.group(1).strip()
    return ""


def _clean_bibliographic_parts(line: str) -> list[str]:
    """Split a citation into comma-separated parts after removing ISBN fragments."""
    line_wo_isbn = re.sub(r"ISBN(?:-1[03])?\s*[:：]?\s*[0-9Xx\-\s]+", "", line, flags=re.I)
    parts = [p.strip(" ,，。") for p in re.split(r",|，", line_wo_isbn) if p.strip(" ,，。")]
    return parts


def _is_year_part(part: str) -> bool:
    return bool(re.fullmatch(r"(?:c?)(?:19|20)\d{2}", part.strip(), flags=re.I))


def _is_publisherish(part: str) -> bool:
    low = part.lower()
    hints = ["press", "publisher", "publishers", "publishing", "university", "springer", "wiley", "oxford", "cambridge"]
    jp_hints = ["出版", "書店", "書房", "館", "社", "培風館", "丸善", "岩波", "講談社", "共立"]
    return any(h in low for h in hints) or any(h in part for h in jp_hints)


def _title_index_from_parts(parts: list[str]) -> int | None:
    if not parts:
        return None
    usable = [(i, p) for i, p in enumerate(parts) if not _is_year_part(p)]
    if not usable:
        return None
    # If the last usable part looks like a publisher, the title is usually just before it.
    last_i, last_p = usable[-1]
    if _is_publisherish(last_p) and len(usable) >= 2:
        return usable[-2][0]
    # Author, Title form: choose the last usable part after author fragments.
    if len(usable) >= 2:
        return usable[-1][0]
    return usable[0][0]


def _extract_english_title(line: str) -> str:
    # Quoted title first.
    m = re.search(r"[\"“]([^\"”]{3,})[\"”]", line)
    if m:
        return m.group(1).strip()
    parts = _clean_bibliographic_parts(line)
    idx = _title_index_from_parts(parts)
    if idx is not None:
        return parts[idx][:160]
    line_wo_isbn = re.sub(r"ISBN(?:-1[03])?\s*[:：]?\s*[0-9Xx\-\s]+", "", line, flags=re.I).strip(" ,，")
    return line_wo_isbn[:120]


def _extract_author(line: str, title: str) -> str:
    if "『" in line and title:
        before = line.split("『", 1)[0].strip(" 著編,，・")
        return before[:120]
    parts = _clean_bibliographic_parts(line)
    idx = _title_index_from_parts(parts)
    if idx is not None and idx > 0:
        return ", ".join(parts[:idx])[:160]
    return ""


def _extract_publisher_year(line: str, title: str) -> tuple[str, str]:
    year = ""
    ym = re.search(r"(19|20)\d{2}", line)
    if ym:
        year = ym.group(0)
    publisher = ""
    if title and title in line:
        after = line.split(title, 1)[-1]
        after = after.strip(" 』」,，。、")
        after = re.sub(r"ISBN.*", "", after, flags=re.I)
        after = re.sub(r"(19|20)\d{2}.*", "", after)
        after = after.strip(" ,，。、")
        # Take the first publisher-looking token.
        if after:
            publisher = re.split(r",|，|。", after)[0].strip()
    return publisher[:120], year


def classify_reference(line: str) -> str:
    low = line.lower()
    if any(h in low for h in NON_BOOK_HINTS):
        if "http" in low or "url" in low:
            return "Web資料"
        return "配付資料"
    if extract_isbn(line):
        return "図書"
    if "雑誌" in line or "journal" in low or "article" in low:
        return "雑誌・論文"
    return "図書候補"


def parse_reference_line(line: str, course: Dict[str, object]) -> Dict[str, object]:
    material_type = classify_reference(line)
    isbn = extract_isbn(line)
    title = _extract_japanese_bracket_title(line) or _extract_english_title(line)
    author = _extract_author(line, title)
    publisher, pub_year = _extract_publisher_year(line, title)
    key = canonical_book_key(title=title, author=author, isbn=isbn)
    confidence = "高" if isbn else ("中" if title and author else "低")
    if material_type in {"配付資料", "Web資料"}:
        confidence = "対象外"
    ref_id = short_hash(course.get("course_id", ""), line)
    return {
        "reference_id": ref_id,
        "canonical_key": key,
        "title": title,
        "author": author,
        "publisher": publisher,
        "publication_year": pub_year,
        "isbn": isbn,
        "material_type": material_type,
        "source_text": line,
        "extraction_confidence": confidence,
    }


def extract_references(courses: pd.DataFrame) -> pd.DataFrame:
    rows = []
    course_cols = [
        "course_id",
        "year",
        "course_number",
        "course_name",
        "instructor",
        "organization",
        "term",
        "weekday_period",
        "syllabus_url",
    ]
    for _, course in courses.iterrows():
        course_dict = {col: course.get(col, "") for col in course_cols}
        for line in split_reference_text(course.get("reference_text", "")):
            ref = parse_reference_line(line, course_dict)
            rows.append({**course_dict, **ref})
    if not rows:
        return pd.DataFrame(
            columns=course_cols
            + [
                "reference_id",
                "canonical_key",
                "title",
                "author",
                "publisher",
                "publication_year",
                "isbn",
                "material_type",
                "source_text",
                "extraction_confidence",
            ]
        )
    return pd.DataFrame(rows)


def aggregate_books(refs: pd.DataFrame) -> pd.DataFrame:
    if refs.empty:
        return pd.DataFrame()
    booklike = refs[~refs["material_type"].isin(["配付資料", "Web資料"])].copy()
    if booklike.empty:
        return pd.DataFrame()
    grouped = (
        booklike.groupby("canonical_key", as_index=False)
        .agg(
            title=("title", "first"),
            author=("author", "first"),
            isbn=("isbn", "first"),
            material_type=("material_type", "first"),
            course_count=("course_id", "nunique"),
            courses=("course_name", lambda x: " / ".join(sorted(set(map(str, x))))),
            instructors=("instructor", lambda x: " / ".join(sorted(set(map(str, x))))),
        )
        .sort_values(["course_count", "title"], ascending=[False, True])
    )
    return grouped
