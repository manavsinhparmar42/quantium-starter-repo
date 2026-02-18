import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load processed dataset
df = pd.read_csv("formatted_output.csv")
df["Date"] = pd.to_datetime(df["Date"])

app = Dash(__name__)
app.title = "Pink Morsel Sales Dashboard"

# ---------------------- LAYOUT ---------------------- #

app.layout = html.Div(
    style={
        "backgroundColor": "#f5f6fa",
        "padding": "40px",
        "fontFamily": "Arial, sans-serif"
    },
    children=[

        html.H1(
            "Soul Foods — Pink Morsel Sales",
            style={
                "textAlign": "center",
                "color": "#2f3640",
                "marginBottom": "30px"
            }
        ),

        html.Div(
            style={
                "textAlign": "center",
                "marginBottom": "25px"
            },
            children=[
                dcc.RadioItems(
                    id="region-selector",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True
                )
            ]
        ),

        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 10px rgba(0,0,0,0.08)"
            },
            children=[
                dcc.Graph(id="sales-graph")
            ]
        )
    ]
)

# ---------------------- CALLBACK ---------------------- #

@app.callback(
    Output("sales-graph", "figure"),
    Input("region-selector", "value")
)
def update_graph(selected_region):

    # Filter by region
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"].str.lower() == selected_region]

    # Aggregate daily sales
    daily_sales = (
        filtered_df
        .groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title="Pink Morsel Sales Over Time",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales",
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_x=0.5
    )

    # Add price increase marker (15 Jan 2021)
    price_date = pd.to_datetime("2021-01-15")

    fig.add_shape(
        type="line",
        x0=price_date,
        x1=price_date,
        y0=daily_sales["Sales"].min(),
        y1=daily_sales["Sales"].max(),
        line=dict(color="red", dash="dash")
    )

    fig.add_annotation(
        x=price_date,
        y=daily_sales["Sales"].max(),
        text="Price Increase (15 Jan 2021)",
        showarrow=True,
        arrowhead=1
    )

    return fig


# ---------------------- RUN APP ---------------------- #

if __name__ == "__main__":
    app.run(debug=True)
