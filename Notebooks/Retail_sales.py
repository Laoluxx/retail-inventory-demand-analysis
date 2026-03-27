import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

df = pd.read_csv("retail_sales_dataset.csv")

df.head()

df.info()

df.describe()

df["Date"] = pd.to_datetime(df["Date"])
df.info()

df.isnull().sum()
df.fillna(0, inplace=True)
df.fillna("Unknown", inplace=True)

total_revenue = df["Total Amount"].sum()
total_quantity = df["Quantity"].sum()

print("Total Revenue:", total_revenue)
print("Total Quantity Sold:", total_quantity)

category_analysis = df.groupby("Product Category").agg({
    "Total Amount": "sum",
    "Quantity": "sum"
}).sort_values(by="Total Amount", ascending=False)

category_analysis

top_products = df.groupby("Product Category").agg({
    "Total Amount": "sum",
    "Quantity": "sum"
}).sort_values(by="Total Amount", ascending=False).head(10)

top_products

slow_products = df.groupby("Product Category").agg({
    "Total Amount": "sum",
    "Quantity": "sum"
}).sort_values(by="Quantity", ascending=True).head(10)

slow_products


df["Inventory"] = df["Quantity"] * np.random.randint(1, 5, size=len(df))

df.head()

inventory_analysis = df.groupby("Product Category").agg({
    "Quantity": "sum",
    "Inventory": "sum"
})

inventory_analysis["Stock_Risk_Percentage"] = (
    inventory_analysis["Quantity"] / inventory_analysis["Inventory"]
) * 100

inventory_analysis = inventory_analysis.sort_values(
    by="Stock_Risk_Percentage", ascending=False
)

inventory_analysis


# Plot stock risk percentage
import matplotlib.pyplot as plt

inventory_analysis["Stock_Risk_Percentage"].plot(kind="bar")

plt.title("Stock Risk Percentage by Product Category (Improved Model)")
plt.xlabel("Product Category")
plt.ylabel("Stock Risk (%)")

plt.xticks(rotation=45)
plt.tight_layout()

# Save 
plt.savefig("visuals/stock_risk_percentage_by_category_updated.png")

plt.show()

# Create visuals folder if it doesn't exist
os.makedirs("visuals", exist_ok=True)

# Create Month column
df["Month"] = df["Date"].dt.to_period("M")

# Aggregate monthly quantity
monthly_demand = df.groupby("Month")["Quantity"].sum()

# Convert to string for plotting
monthly_demand.index = monthly_demand.index.astype(str)

# Plot
monthly_demand.plot()

plt.title("Monthly Demand Trend")
plt.xlabel("Month")
plt.ylabel("Total Quantity Sold")

plt.xticks(rotation=45)
plt.tight_layout()

# Save plot
plt.savefig("visuals/monthly_demand_trend.png")

plt.show()

df.to_csv("data/cleaned_retail_data.csv", index=False)