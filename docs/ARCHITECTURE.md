# Architecture — Smart CSV Profiler

```mermaid
flowchart LR
    A["customer_data.csv"] --> B["profile_csv.py"]
    B --> C["profile.json"]
```

## Inputs

- `sample/customer_data.csv`

## Source files

- `src/profile_csv.py`

## Output

- `results/artifacts/profile.json`

This representation is intended for source navigation. It does not imply a production deployment or undisclosed components. The editable diagram is available as [`architecture.mmd`](architecture.mmd).
