# Decisions log

Each entry records a choice between two or more approaches, the one taken, and why.

## 1. Ingestion runs on the laptop and in GitHub Actions, not in Databricks notebooks

Databricks Free Edition restricts outbound internet access, so notebooks cannot call the WHO or World Bank APIs without LinkedIn verification. Ingestion scripts live in the repo and run in plain Python; Databricks is the warehouse, not the scheduler. This also keeps fetch and load as separate, rerunnable steps.

## 2. Raw API responses are saved to disk before anything else touches them

Each fetch writes the unmodified response to data/raw/<source>/ with a UTC timestamp in the filename. Silver logic will be wrong at first, and re-running from a local file is faster and kinder to the API than re-downloading. This is the bronze principle applied before the data reaches Databricks.