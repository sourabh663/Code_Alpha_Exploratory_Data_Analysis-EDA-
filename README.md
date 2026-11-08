# Task 2: Exploratory Data Analysis (EDA)

## Project overview
This project performs exploratory data analysis on the book dataset created in Task 1 (web scraping). It explores data types, missing values, duplicates, distributions, rating counts, and the relationship between price and rating.

## Research questions
1. What is the structure and data type of each variable?
2. What is the typical book price (mean and median)?
3. How are books distributed across star ratings?
4. Is there an apparent relationship between price and rating?
5. Are there missing values, duplicate rows, or values outside expected ranges?

## Tools
- Python
- Pandas
- Matplotlib

## Run the project
1. Install Python 3.9+.
2. Install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run using the included preview:
   ```bash
   python eda.py
   ```
4. To analyze the full dataset from Task 1:
   ```bash
   python eda.py path/to/books_dataset.csv
   ```

## Output files
- `output/cleaned_books_dataset.csv` — duplicate rows removed and numeric fields prepared.
- `output/numeric_summary.csv` — descriptive statistics.
- `output/missing_values.csv` — missing-value counts.
- `output/eda_findings.json` — machine-readable findings.
- `output/plots/` — price distribution, rating counts, and price-rating scatter plot.

## Important limitation
The bundled input is the small sample preview from Task 1, not the complete catalogue. The sample is sufficient to demonstrate the EDA workflow, but it is too small for strong statistical conclusions or generalization. For a meaningful final analysis, run Task 1's scraper to collect the full catalogue, then run this script on that CSV. Correlation is descriptive and does not establish causation.
