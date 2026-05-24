from __future__ import annotations

import io
from typing import BinaryIO

import pandas as pd

from .utils import first_existing_column, short_hash


COLUMN_CANDIDATES = {
    "year": ["年度", "Academic year", "academic_year", "year", "履修年度"],
    "course_number": ["科目番号", "Course Number", "course_number", "courseNo", "科目コード", "科目No"],
    "course_name": ["科目名", "Course Name", "course_name", "name", "授業科目名"],
    "instructor": ["担当教員", "Instructor", "instructor", "教員", "担当", "担当教員名"],
    "organization": ["組織", "Organization", "organization", "開設組織", "教育組織", "学群", "学位プログラム"],
    "term": ["開講時期", "Term", "term", "学期", "モジュール", "開講学期"],
    "weekday_period": ["曜時限", "Weekday and Period", "weekday_period", "曜日時限", "時限", "曜日・時限"],
    "credits": ["単位数", "Credits", "credits", "単位"],
    "syllabus_url": ["Syllabus URL", "syllabus_url", "URL", "シラバスURL", "詳細URL"],
    "reference_text": [
        "教材・参考文献・配付資料等",
        "教材・参考文献・配布資料等",
        "教材・参考文献・配付資料",
        "教材・参考文献",
        "参考文献",
        "教材",
        "Course Materials",
        "Teaching Materials",
        "Materials/Reference",
        "reference_text",
        "syllabus",
    ],
}


def read_uploaded_table(file: BinaryIO, filename: str) -> pd.DataFrame:
    lower = filename.lower()
    if lower.endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    # Try common Japanese encodings after UTF-8.
    raw = file.read()
    for encoding in ("utf-8-sig", "utf-8", "cp932", "shift_jis"):
        try:
            return pd.read_csv(io.BytesIO(raw), encoding=encoding)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(io.BytesIO(raw))


def standardize_courses(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    out = pd.DataFrame()
    for target, candidates in COLUMN_CANDIDATES.items():
        col = first_existing_column(df.columns, candidates)
        if col is not None:
            out[target] = df[col]
        else:
            out[target] = ""

    # Normalize missing values to empty strings for UI friendliness.
    out = out.fillna("")

    # Create stable course_id.
    if (out["course_number"].astype(str).str.strip() != "").any():
        out["course_id"] = out.apply(
            lambda r: str(r["course_number"]).strip()
            or short_hash(r["year"], r["course_name"], r["instructor"]),
            axis=1,
        )
    else:
        out["course_id"] = out.apply(
            lambda r: short_hash(r["year"], r["course_name"], r["instructor"]),
            axis=1,
        )

    ordered = [
        "course_id",
        "year",
        "course_number",
        "course_name",
        "instructor",
        "organization",
        "term",
        "weekday_period",
        "credits",
        "syllabus_url",
        "reference_text",
    ]
    return out[ordered]


def sample_courses() -> pd.DataFrame:
    data = [
        {
            "course_id": "0A00001",
            "year": "2026",
            "course_number": "0A00001",
            "course_name": "量子情報科学",
            "instructor": "サンプル 太郎",
            "organization": "理工情報生命学術院",
            "term": "秋AB",
            "weekday_period": "火3,4",
            "credits": "2.0",
            "syllabus_url": "",
            "reference_text": "Nielsen, M. A. and Chuang, I. L., Quantum Computation and Quantum Information, Cambridge University Press, ISBN 9781107002173\nJohn Watrous, The Theory of Quantum Information, Cambridge University Press, 2018, ISBN 9781107180567\n必要に応じてmanabaで資料を配付する。",
        },
        {
            "course_id": "0A00002",
            "year": "2026",
            "course_number": "0A00002",
            "course_name": "量子力学特論",
            "instructor": "サンプル 花子",
            "organization": "理工情報生命学術院",
            "term": "春AB",
            "weekday_period": "月5,6",
            "credits": "2.0",
            "syllabus_url": "",
            "reference_text": "J. J. Sakurai and Jim Napolitano, Modern Quantum Mechanics, Cambridge University Press, ISBN 9781108473224\nNielsen, M. A. and Chuang, I. L., Quantum Computation and Quantum Information, Cambridge University Press, ISBN 9781107002173",
        },
        {
            "course_id": "0A00003",
            "year": "2026",
            "course_number": "0A00003",
            "course_name": "統計物理学",
            "instructor": "サンプル 次郎",
            "organization": "理工情報生命学術院",
            "term": "春C",
            "weekday_period": "金3,4",
            "credits": "1.0",
            "syllabus_url": "",
            "reference_text": "田崎晴明『統計力学 I』培風館, 2008, ISBN 9784563024376\n授業中に資料を配布する。",
        },
    ]
    return pd.DataFrame(data)
