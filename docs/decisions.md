# Decisions log

Each entry records a choice between two or more approaches, the one taken, and why.

## 1. Ingestion runs on the laptop and in GitHub Actions, not in Databricks notebooks

Databricks Free Edition restricts outbound internet access, so notebooks cannot call the WHO or World Bank APIs without LinkedIn verification. Ingestion scripts live in the repo and run in plain Python; Databricks is the warehouse, not the scheduler. This also keeps fetch and load as separate, rerunnable steps.

## 2. Raw API responses are saved to disk before anything else touches them

Each fetch writes the unmodified response to data/raw/<source>/ with a UTC timestamp in the filename. Silver logic will be wrong at first, and re-running from a local file is faster and kinder to the API than re-downloading. This is the bronze principle applied before the data reaches Databricks.

## 3. One bronze table per OWID chart instead of one combined table

The three OWID CSVs have different value column names (life_expectancy_0, child_mortality_rate, coverage__antigen_mcv1). Combining them in bronze would mean either a sparse table with three mostly-null columns or reshaping to a long format, and reshaping is a transformation. Bronze stays a faithful copy, so each chart gets its own table and silver does the reshaping.

## 4. Notebooks live in the repo through a Databricks Git folder

Notebooks created in the workspace only exist there, and Free Edition accounts can be deleted after inactivity. The repo is cloned into Databricks as a Git folder, notebooks are committed from there, and the laptop pulls them. One repo holds ingestion scripts, notebooks and docs.