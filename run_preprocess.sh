#!/usr/bin/env bash
set -euo pipefail

# Runner for preprocess_sales.py
# Adjust paths below if your files live elsewhere.

python preprocess_sales.py   --sales2017 "./data/sales 2017.xlsx"   --sales2018 "./data/sales 2018.xlsx"   --sales2019 "./data/sales 2019.xlsx"   --outdir "./data"   --train_end "2019-04-01"   --test_start "2019-05-01"
