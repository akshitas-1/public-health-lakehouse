
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