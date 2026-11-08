"""
Task 2: Exploratory Data Analysis (EDA)
Input: output/books_dataset_for_eda.csv by default, or pass a CSV path:
    python eda.py path/to/books_dataset.csv

Outputs are written to output/:
- cleaned_books_dataset.csv
- numeric_summary.csv
- missing_values.csv
- eda_findings.json
- plots/*.png
"""
from pathlib import Path
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt

INPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/books_dataset_for_eda.csv")
OUTPUT = Path("output")
PLOTS = OUTPUT / "plots"

def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Cannot find {INPUT}. Copy the Task 1 CSV here or pass its path as an argument."
        )

    OUTPUT.mkdir(exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(INPUT)
    data.columns = [str(c).strip().lower().replace(" ", "_") for c in data.columns]

    # Convert displayed currency strings (for example £51.77) into numeric values.
    if "price" in data.columns:
        data["price_numeric"] = (
            data["price"].astype(str).str.replace(r"[^0-9.]", "", regex=True)
            .replace("", pd.NA).astype(float)
        )

    # Convert word ratings to numeric values if needed.
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    if "rating_numeric" not in data.columns and "rating" in data.columns:
        data["rating_numeric"] = data["rating"].map(rating_map)

    rows_before = len(data)
    duplicate_rows = int(data.duplicated().sum())
    data = data.drop_duplicates().copy()

    # Flag, but do not silently delete, implausible values.
    issues = []
    if "price_numeric" in data.columns:
        if (data["price_numeric"] < 0).any():
            issues.append("Negative book prices detected.")
    if "rating_numeric" in data.columns:
        if (~data["rating_numeric"].dropna().between(1, 5)).any():
            issues.append("Ratings outside the expected 1–5 range detected.")

    data.to_csv(OUTPUT / "cleaned_books_dataset.csv", index=False, encoding="utf-8-sig")
    data.select_dtypes(include="number").describe().round(2).to_csv(
        OUTPUT / "numeric_summary.csv"
    )
    data.isna().sum().rename("missing_values").to_csv(OUTPUT / "missing_values.csv")

    # Price histogram
    if "price_numeric" in data.columns and data["price_numeric"].notna().any():
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.hist(data["price_numeric"].dropna(), bins=15)
        ax.set(title="Distribution of Book Prices", xlabel="Price", ylabel="Number of books")
        fig.tight_layout()
        fig.savefig(PLOTS / "price_distribution.png", dpi=150)
        plt.close(fig)

    # Rating counts
    if "rating_numeric" in data.columns and data["rating_numeric"].notna().any():
        counts = data["rating_numeric"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.bar(counts.index.astype(str), counts.values)
        ax.set(title="Book Counts by Star Rating", xlabel="Rating (1–5 stars)", ylabel="Number of books")
        fig.tight_layout()
        fig.savefig(PLOTS / "rating_counts.png", dpi=150)
        plt.close(fig)

    # Price-rating scatter plot
    if {"price_numeric", "rating_numeric"}.issubset(data.columns):
        pair = data[["price_numeric", "rating_numeric"]].dropna()
        if len(pair) >= 2:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.scatter(pair["rating_numeric"], pair["price_numeric"])
            ax.set(title="Book Price vs. Star Rating", xlabel="Rating (1–5 stars)", ylabel="Price")
            fig.tight_layout()
            fig.savefig(PLOTS / "price_vs_rating.png", dpi=150)
            plt.close(fig)

    findings = {
        "rows_before_deduplication": rows_before,
        "rows_after_deduplication": len(data),
        "duplicate_rows_removed": duplicate_rows,
        "columns": list(data.columns),
        "missing_values_by_column": data.isna().sum().to_dict(),
        "data_quality_flags": issues,
        "note": "Correlation and visual patterns are descriptive, not proof of causation."
    }
    if "price_numeric" in data.columns:
        findings["mean_price"] = round(float(data["price_numeric"].mean()), 2)
        findings["median_price"] = round(float(data["price_numeric"].median()), 2)
    if "rating_numeric" in data.columns:
        findings["mean_rating"] = round(float(data["rating_numeric"].mean()), 2)
    if {"price_numeric", "rating_numeric"}.issubset(data.columns):
        pair = data[["price_numeric", "rating_numeric"]].dropna()
        if len(pair) >= 2 and pair["price_numeric"].nunique() > 1 and pair["rating_numeric"].nunique() > 1:
            findings["price_rating_correlation"] = round(
                float(pair["price_numeric"].corr(pair["rating_numeric"])), 3
            )

    (OUTPUT / "eda_findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
    print(f"EDA complete: {len(data)} rows analyzed.")
    print(f"Outputs saved in: {OUTPUT.resolve()}")
    print("Review the sample-size limitation before interpreting results.")

if __name__ == "__main__":
    main()
