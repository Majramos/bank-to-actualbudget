# Bank to Actualbudget

**bank-to-actualbudget** is a lightweight automation tool designed to bridge the gap between messy banking exports and clean, actionable budget data. It parses unstructured PDF or CSV bank statements and transforms them into standardized, [ActualBudget](https://actualbudget.org/) compatible CSV files.

## Setup & Installation

This project uses uv for ultra-fast Python package and project management.

1. Install uv (if you haven't already):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. Clone and Sync:
```bash
git clone https://gitlab.com/majramos/bank-to-actualbudget.git
cd bank-to-actualbudget
uv sync
```

## How to use

To run the converter using the managed virtual environment:

1. Run the script via uv run:
```bash
uv run bank-to-actualbudget <name of the file>
```
2. Find your formatted file in the `/output` folder and drag it into Actual Budget.

## Suported Banks
- TODO
