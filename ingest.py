from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Iterable, Optional


def normalize_text(value: object) -> str:
    """Normalize Japanese/English text for loose matching."""
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value))
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def compact_text(value: object) -> str:
    text = normalize_text(value)
    return re.sub(r"[\s\-:：,，.。;；/／\\()（）\[\]【】『』「」'\"]+", "", text)


def short_hash(*parts: object, length: int = 12) -> str:
    raw = "|".join(str(p) for p in parts if p is not None)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:length]


def normalize_isbn(value: object) -> str:
    """Return a compact ISBN-like string. No checksum validation is performed."""
    if value is None:
        return ""
    s = unicodedata.normalize("NFKC", str(value)).upper()
    s = re.sub(r"[^0-9X]", "", s)
    if len(s) in (10, 13):
        return s
    # Sometimes OCR/citations include multiple digits around ISBN. Keep the first valid length.
    m13 = re.search(r"97[89][0-9]{10}", s)
    if m13:
        return m13.group(0)
    m10 = re.search(r"[0-9]{9}[0-9X]", s)
    if m10:
        return m10.group(0)
    return ""


ISBN_PATTERN = re.compile(
    r"(?:ISBN(?:-1[03])?\s*[:：]?\s*)?((?:97[89][\-\s]?)?[0-9][0-9Xx][0-9Xx\-\s]{7,17}[0-9Xx])"
)


def extract_isbn(text: object) -> str:
    if text is None:
        return ""
    s = unicodedata.normalize("NFKC", str(text))
    for match in ISBN_PATTERN.finditer(s):
        isbn = normalize_isbn(match.group(1))
        if isbn:
            return isbn
    return ""


def first_existing_column(columns: Iterable[str], candidates: Iterable[str]) -> Optional[str]:
    columns_list = list(columns)
    normalized = {compact_text(c): c for c in columns_list}
    for candidate in candidates:
        key = compact_text(candidate)
        if key in normalized:
            return normalized[key]
    # partial match fallback
    for candidate in candidates:
        key = compact_text(candidate)
        for col in columns_list:
            ckey = compact_text(col)
            if key and (key in ckey or ckey in key):
                return col
    return None


def canonical_book_key(title: object = "", author: object = "", isbn: object = "") -> str:
    clean_isbn = normalize_isbn(isbn)
    if clean_isbn:
        return f"isbn:{clean_isbn}"
    t = compact_text(title)
    a = compact_text(author)
    if t and a:
        return f"ta:{t[:80]}:{a[:40]}"
    if t:
        return f"title:{t[:120]}"
    return "unknown"


def csv_bytes(df) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")
