# Execution record — Smart CSV Profiler

**Status:** Local execution completed using bundled fixtures.  
**Python:** 3.13.5  
**Execution time:** 1.59 seconds in the packaging environment (not a standardized benchmark).  
**Method:** `python src/profile_csv.py sample/customer_data.csv --output outputs/profile.json`

## Observed output

![Observed output](../assets/result.svg)

| Field | Observed value |
|:--|--:|
| Rows | 5 |
| Columns | 5 |
| Duplicate rows | 1 |

**Raw output:** [execution.txt](../results/execution.txt)  
**Command records and SHA-256 digests:** [execution.json](../results/execution.json)

## Interpretation

Results were computed on the included test fixtures. They demonstrate one successful invocation, not measured generalization, comparative performance, system availability or operational readiness. If the fixtures or application are synthetic, values remain synthetic or simulated.
