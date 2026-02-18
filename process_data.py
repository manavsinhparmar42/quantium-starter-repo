import pandas as pd

# Step 1: Load the three CSV files
df1 = pd.read_csv("data/daily_sales_data_0.csv")
df2 = pd.read_csv("data/daily_sales_data_1.csv")
df3 = pd.read_csv("data/daily_sales_data_2.csv")

# Step 2: Combine them into one dataframe
df = pd.concat([df1, df2, df3], ignore_index=True)

# Step 3: Filter only Pink Morsel
df = df[df["product"] == "Pink Morsel"]

# Step 4: Create Sales column
df["Sales"] = df["quantity"] * df["price"]

# Step 5: Select required columns
final_df = df[["Sales", "date", "region"]]

# Step 6: Rename columns properly
final_df = final_df.rename(columns={
    "date": "Date",
    "region": "Region"
})

# Step 7: Save output file
final_df.to_csv("formatted_output.csv", index=False)

print("Data successfully processed and saved.")
