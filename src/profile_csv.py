from __future__ import annotations
import argparse, json, re
from pathlib import Path
import numpy as np
import pandas as pd

EMPTY_LIKE = {"", "na", "n/a", "null", "none", "unknown", "-", "--"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
URL_RE = re.compile(r"^https?://", re.I)

def semantic_type(s: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(s): return "boolean"
    if pd.api.types.is_numeric_dtype(s): return "numeric"
    if pd.api.types.is_datetime64_any_dtype(s): return "datetime"
    nonnull = s.dropna()
    if nonnull.empty: return "empty"
    # conservative datetime inference only for date-shaped strings
    text = nonnull.astype(str).str.strip()
    date_like = text.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}")
    if date_like.mean() >= 0.9:
        parsed = pd.to_datetime(text, errors="coerce")
        if parsed.notna().mean() >= 0.9: return "datetime"
    ratio = nonnull.nunique(dropna=True) / max(len(nonnull), 1)
    avg_len = nonnull.astype(str).str.len().mean()
    if ratio <= 0.2 and nonnull.nunique() <= 100: return "categorical"
    return "text" if avg_len > 25 else "categorical"

def numeric_outliers(s: pd.Series) -> dict:
    x = pd.to_numeric(s, errors="coerce").dropna()
    if len(x) < 4:
        return {"count": 0, "lower_bound": None, "upper_bound": None}
    q1, q3 = x.quantile([0.25, 0.75])
    iqr = q3 - q1
    if iqr == 0:
        return {"count": 0, "lower_bound": float(q1), "upper_bound": float(q3)}
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return {"count": int(((x < low) | (x > high)).sum()),
            "lower_bound": float(low), "upper_bound": float(high)}

def suspicious_strings(s: pd.Series) -> dict:
    vals = s.dropna().astype(str).str.strip()
    lower = vals.str.lower()
    return {
        "empty_like_tokens": int(lower.isin(EMPTY_LIKE).sum()),
        "email_like": int(vals.map(lambda v: bool(EMAIL_RE.match(v))).sum()),
        "url_like": int(vals.map(lambda v: bool(URL_RE.match(v))).sum()),
        "very_long_strings": int((vals.str.len() > 250).sum()),
    }

def profile_dataframe(df: pd.DataFrame) -> dict:
    report = {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_profiles": {}
    }
    for col in df.columns:
        s = df[col]
        st = semantic_type(s)
        item = {
            "dtype": str(s.dtype),
            "semantic_type": st,
            "missing_count": int(s.isna().sum()),
            "missing_percent": round(float(s.isna().mean() * 100), 3),
            "unique_count": int(s.nunique(dropna=True)),
            "unique_percent": round(float(s.nunique(dropna=True) / max(len(s), 1) * 100), 3),
        }
        if st == "numeric":
            item["outliers"] = numeric_outliers(s)
            x = pd.to_numeric(s, errors="coerce")
            item["summary"] = {
                "min": None if x.dropna().empty else float(x.min()),
                "max": None if x.dropna().empty else float(x.max()),
                "mean": None if x.dropna().empty else float(x.mean()),
                "median": None if x.dropna().empty else float(x.median()),
            }
        else:
            item["suspicious_values"] = suspicious_strings(s)
            top = s.dropna().astype(str).value_counts().head(5)
            item["top_values"] = {str(k): int(v) for k, v in top.items()}
        report["column_profiles"][str(col)] = item
    return report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--output", default="profile.json")
    ap.add_argument("--encoding", default="utf-8")
    args = ap.parse_args()
    df = pd.read_csv(args.csv, encoding=args.encoding)
    report = profile_dataframe(df)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
