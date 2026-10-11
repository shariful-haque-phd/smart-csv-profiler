# Smart CSV Profiler

A lightweight command-line profiler for CSV datasets. It detects inferred column types, missing values, duplicate rows, numeric outliers, cardinality, and suspicious string patterns, then writes a machine-readable JSON report.

## Features
- CSV shape and duplicate-row summary
- Inferred semantic types: numeric, datetime, boolean, categorical, text
- Missing-value and uniqueness statistics
- IQR-based numeric outlier counts
- Suspicious-value detection for empty-like tokens, URLs, emails, and unusually long strings
- JSON output suitable for CI/data-pipeline checks

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/profile_csv.py sample/customer_data.csv --output outputs/profile.json
```

## Why this exists
Data issues are often discovered after modeling or reporting has already started. This tool gives a fast first-pass health check that can be automated before downstream processing.

## Notes
Outlier and suspicious-value rules are heuristics. They are intended to flag records for review, not to decide that a value is wrong.
