# Research brief — Smart CSV Profiler

**Area:** Data Foundations & Engineering  
**Portfolio level:** Foundations

## Research problem

A lightweight command-line profiler for CSV datasets. It detects inferred column types, missing values, duplicate rows, numeric outliers, cardinality, and suspicious string patterns, then writes a machine-readable JSON report.

## Question

How reliably can inexpensive column-level statistics flag dataset issues before downstream processing?

## Implementation scope

- CSV shape and duplicate-row summary
- Inferred semantic types: numeric, datetime, boolean, categorical, text
- Missing-value and uniqueness statistics
- IQR-based numeric outlier counts
- Suspicious-value detection for empty-like tokens, URLs, emails, and unusually long strings
- JSON output suitable for CI/data-pipeline checks

### Reproducible inputs and outputs

The current baseline uses `sample/customer_data.csv`. The implementation consists of `src/profile_csv.py`. Execution records, where available, are retained in [`results/`](../results/).

## Evaluation plan

1. Establish a versioned data protocol, input schema and independent baseline.
2. Evaluate functional correctness and record both successful and failed cases.
3. Compare relevant outcomes under controlled input variations and fixed environment settings.
4. Measure resource use and execution time across replicates when meaningful.
5. Document limitations, data provenance and risks of deployment in consequential environments.

### Validity and scope

The included local inputs are not evidence of population-level accuracy or external impact. Any synthetic inputs, simulations, heuristics and estimated performance figures must remain explicitly identified. Future benchmarks should use representative datasets, appropriate baselines, pre-specified metrics and independently reviewed methods.

## Evidence

Refer to [the recorded run](RESULTS.md), or to [the original project instructions](ORIGINAL_README.md) where local execution is not established. No publication, patent, user adoption or real-world deployment is claimed.
