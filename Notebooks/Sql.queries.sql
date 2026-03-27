import sqlite3
import pandas as pd
import numpy as np


# Load the cleaned CSV
df = pd.read_csv(r"C:\Users\user\Downloads\project_folder\Retail_inventory_demand_analysis\Data\cleaned_retail_data.csv")

# Create SQLite database
conn = sqlite3.connect(r"C:\Users\user\Downloads\project_folder\Retail_inventory_demand_analysis\retail_inventory.db")

# Export dataframe to SQL table
df.to_sql("retail_sales", conn, if_exists="replace", index=False)

print("Table loaded successfully.")


# Recreate inventory
df["Inventory"] = df["Quantity"] * np.random.randint(1, 5, size=len(df))

# Push updated dataframe to SQL again
df.to_sql("retail_sales", conn, if_exists="replace", index=False)

print("Inventory column added and table updated.")


query = """
SELECT 
    SUM("Total Amount") AS total_revenue,
    SUM(Quantity) AS total_quantity
FROM retail_sales
"""

result = pd.read_sql(query, conn)
result

query = """
SELECT 
    "Product Category",
    SUM("Total Amount") AS total_revenue,
    SUM(Quantity) AS total_quantity
FROM retail_sales
GROUP BY "Product Category"
ORDER BY total_revenue DESC
"""

category_sql = pd.read_sql(query, conn)
category_sql

query = """
SELECT 
    "Product Category",
    SUM("Total Amount") AS total_revenue,
    SUM(Quantity) AS total_quantity,
    RANK() OVER (ORDER BY SUM("Total Amount") DESC) AS revenue_rank
FROM retail_sales
GROUP BY "Product Category"
"""

ranked_categories = pd.read_sql(query, conn)
ranked_categories


query = """
SELECT
    "Product Category",
    SUM(Quantity) AS total_quantity,
    SUM(Inventory) AS total_inventory,
    ROUND((SUM(Quantity) * 100.0) / SUM(Inventory), 2) AS stock_risk_percentage
FROM retail_sales
GROUP BY "Product Category"
ORDER BY stock_risk_percentage DESC
"""

stock_risk_sql = pd.read_sql(query, conn)
stock_risk_sql

query = """
SELECT
    strftime('%Y-%m', Date) AS month,
    SUM(Quantity) AS total_quantity,
    SUM("Total Amount") AS total_revenue
FROM retail_sales
GROUP BY strftime('%Y-%m', Date)
ORDER BY month
"""

monthly_sql = pd.read_sql(query, conn)
monthly_sql