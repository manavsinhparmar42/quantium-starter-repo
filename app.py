import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load processed data
df = pd.read_csv("formatted_output.csv")

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Group by Date and sum Sales
daily_sales = df.groupby("Date")["Sales"].sum().reset_index()

# Sort by Date
daily_sales = daily_sales.sort_values("Date")

# Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time"
)

# Update axis labels
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales"
)

# Add vertical line manually (stable method)
price_increase_date = pd.to_datetime("2021-01-15")

fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=daily_sales["Sales"].min(),
    y1=daily_sales["Sales"].max(),
    line=dict(color="red", dash="dash")
)

# Add annotation text
fig.add_annotation(
    x=price_increase_date,
    y=daily_sales["Sales"].max(),
    text="Price Increase (15 Jan 2021)",
    showarrow=True,
    arrowhead=1
)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
