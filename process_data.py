import pandas as pd

# Step 1: Load the three CSV files
df1 = pd.read_csv("data/daily_sales_data_0.csv")
df2 = pd.read_csv("data/daily_sales_data_1.csv")
df3 = pd.read_csv("data/daily_sales_data_2.csv")

# Step 2: Combine them into one dataframe
df = pd.concat([df1, df2, df3], ignore_index=True)

# Step 3: Clean column names (safety step)
df.columns = df.columns.str.strip().str.lower()

# Step 4: Keep only Pink Morsel (case insensitive + remove extra spaces)
df["product"] = df["product"].str.strip().str.lower()
df = df[df["product"] == "pink morsel"]

# Step 5: Clean price column (remove $ sign and convert to float)
df["price"] = df["price"].replace(r'[\$,]', '', regex=True).astype(float)

# Step 6: Ensure quantity is numeric
df["quantity"] = pd.to_numeric(df["quantity"])

# Step 7: Create Sales column
df["sales"] = df["quantity"] * df["price"]

# Step 8: Select required columns
final_df = df[["sales", "date", "region"]]

# Step 9: Rename columns properly
final_df = final_df.rename(columns={
    "sales": "Sales",
    "date": "Date",
    "region": "Region"
})

# Step 10: Save output file
final_df.to_csv("formatted_output.csv", index=False)

print("Data successfully processed and saved.")
