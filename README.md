
# Public health data lakehouse with an AI query layer

A medallion-architecture lakehouse on Databricks Free Edition that ingests three public health sources with different shapes, reconciles them, flags anomalies, and exposes the result to an LLM through an MCP server with an evaluation harness.

Built in public as a portfolio project. Every number in this README comes from a real run.

## Problem

Global health analysts pull the same indicators (life expectancy, under-5 mortality, measles vaccine coverage) from WHO, the World Bank and Our World in Data. The three sources disagree on country names and codes, on which years are covered, on units, and on how missing data is represented. Analysts reconcile this by hand in spreadsheets, and when a manager asks "which countries had a drop in measles coverage last year", the answer depends on which spreadsheet was open. This project builds the reconciled layer once and puts a natural-language interface on top that can be measured for accuracy rather than demoed.

## Who it is for

- A program analyst who needs one trustworthy number per country per year per indicator, with a record of where it came from.
- A program manager who wants to ask questions in plain English and know when the answer should be checked by a human.
- A hiring manager who wants to see that I can reason about ingestion, reconciliation, governance and LLM evaluation with working code.

## Architecture

```mermaid
flowchart LR
    WHO[WHO GHO API<br/>single JSON response] --> F[Fetch scripts<br/>Python, laptop or GitHub Actions]
    WB[World Bank API<br/>paginated JSON] --> F
    OWID[Our World in Data<br/>CSV download] --> F
    F


    ## Findings from bronze, before any cleaning

Comparing life expectancy for 2019 across the three sources for every country all three cover:

- The World Bank and OWID values are identical in every row, because both take the figure from UN World Population Prospects. There are two independent estimates here, not three.
- The largest disagreement between WHO and the UN-derived value is Central African Republic: 52.9 versus 31.5, a spread of 21.4 years. Nigeria is next at 10.1.

Looking at Central African Republic year by year:

| year | WHO | World Bank |
|---|---|---|
| 2018 | 52.1 | 52.3 |
| 2019 | 52.9 | 31.5 |
| 2020 | 53.1 | 50.6 |
| 2021 | 52.3 | 40.3 |
| 2022 | | 18.8 |
| 2023 | | 57.4 |

The WHO series moves by fractions of a year, which is how life expectancy behaves. The World Bank series swings by 20 to 40 years between adjacent years. A year-on-year change threshold would flag every one of those rows. This is the first anomaly the project found, and it was found by looking, before any detection code was written.

Query: `notebooks/02_source_comparison.ipynb`.