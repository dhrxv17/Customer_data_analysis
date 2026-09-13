# Customer Shopping Behavior Analysis

An end-to-end data analytics project that takes raw retail transaction data through cleaning and feature engineering in **Python**, storage in **PostgreSQL**, and visualization in **Power BI**.

**Tech stack:** Python (pandas) &rarr; PostgreSQL (SQLAlchemy) &rarr; Power BI

---

## Project Overview

This project analyzes ~3,900 customer shopping transactions to uncover patterns in purchase amount, category preference, subscription behavior, and customer demographics. It demonstrates a complete analytics workflow:

1. **Extract** – load the raw CSV export
2. **Transform** – clean missing values, engineer new features, standardize schema
3. **Load** – push the cleaned dataset into a PostgreSQL database
4. **Visualize** – build an interactive Power BI dashboard on top of the database

## Dataset

- **Source:** Customer shopping transaction records (`customer_shopping_behavior.csv`)
- **Size:** 3,900 rows × 18 columns
- **Fields:** customer ID, age, gender, item purchased, category, purchase amount, location, size, color, season, review rating, subscription status, shipping type, discount applied, previous purchases, payment method, frequency of purchases

## Data Cleaning & Feature Engineering

| Step | Detail |
|---|---|
| **Missing values** | `review_rating` had 37 nulls. Rather than fill with a single global mean (which can be skewed by outliers), missing values are imputed with the **median rating within each product category**. |
| **Schema cleanup** | Column names standardized to `lower_snake_case`; `purchase_amount_(usd)` renamed to `purchase_amount`. |
| **Redundant column removal** | `discount_applied` and `promo_code_used` were identical in every row, so the duplicate column is dropped. |
| **Feature: `age_group`** | Customers bucketed into quartile-based groups: `young`, `adult`, `middle_aged`, `senior` (via `pd.qcut`). |
| **Feature: `purchase_frequency_days`** | The text field `frequency_of_purchases` (e.g. "Weekly", "Monthly") is mapped to a numeric day count, making it usable for numeric analysis (e.g. RFM-style churn signals). |

## Pipeline / ETL

`customer_shopping_etl.py` reads the CSV, applies the cleaning steps above, and loads the result into a PostgreSQL table (`customer` in the `customer_behavior` database) using SQLAlchemy.

Credentials are read from environment variables (see `.env.example`) rather than hardcoded, so the script is safe to publish on GitHub.

```bash
pip install -r requirements.txt
cp .env.example .env        # fill in your local PostgreSQL credentials
python customer_shopping_etl.py
```

`Main.ipynb` contains the same logic in notebook form, useful for exploring the data step by step (nulls check, dtype checks, etc. are left as comments showing the exploration process).

## Power BI Dashboard

`power_bi_present.pbix` connects to the PostgreSQL `customer` table and includes:

- **KPI cards:** total number of customers, average purchase amount, average review rating
- **Category spend:** clustered column charts of average purchase amount by category
- **Age group breakdown:** clustered bar charts of customer count and purchase amount by age group
- **Subscription mix:** donut chart of subscribers vs. non-subscribers
- **Slicers:** filter the whole page by category, gender, subscription status, and shipping type

### Key insights surfaced by the dashboard

- Clothing (1,737) and Accessories (1,240) are the two dominant categories, together making up ~76% of transactions.
- Average purchase amount is fairly consistent across categories (~$57–60), suggesting spend is driven more by item count than category-specific pricing.
- Only ~27% of customers are active subscribers.
- Average review rating across the dataset is 3.75 / 5.

## Repository Structure

```
├── customer_shopping_behavior.csv   # raw dataset
├── customer_shopping_etl.py         # cleaning + PostgreSQL load script (production-ready)
├── Main.ipynb                       # exploratory notebook version of the same pipeline
├── power_bi_present.pbix            # Power BI dashboard
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How to Run This Project

1. Clone the repo and install dependencies: `pip install -r requirements.txt`
2. Install PostgreSQL locally (or point `.env` at a remote instance) and create a database named `customer_behavior`
3. Copy `.env.example` to `.env` and fill in your credentials
4. Run `python customer_shopping_etl.py` to load the cleaned data into PostgreSQL
5. Open `power_bi_present.pbix` in Power BI Desktop, update the data source connection to your PostgreSQL instance, and refresh

## Possible Extensions

- Add SQL views/queries (RFM segmentation, cohort analysis) directly in PostgreSQL
- Publish the Power BI report to the Power BI Service and embed a link/screenshot here
- Add unit tests for the cleaning functions in `customer_shopping_etl.py`

---

*Author: [Your Name] — feel free to connect on [LinkedIn](#) or check out more projects on [GitHub](#).*

Publish the Power BI report to the Power BI Service and embed a link/screenshot here
Add unit tests for the cleaning functions in customer_shopping_etl.py
