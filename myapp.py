# Task 4- A Dashboard with Dash

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.data as pldata


df = px.data.gapminder() #columns: country continent  year  lifeExp pop   gdpPercap iso_alpha  iso_num

print(df.head())
print(df.columns)

countries = df["country"].unique() # countries = df["country"].drop_duplicates()


# Initialize Dash app
app = Dash(__name__)
server = app.server

# Layout
app.layout = html.Div(
    children=[
        html.H1("Gapminder Country Dashboard"),

        dcc.Dropdown(                         
            id="country-dropdown",
            options=[{"label": c, "value": c} for c in countries],
            value="Canada",           
            clearable=False,
            style={"width": "300px"},
        ),
        dcc.Graph(id="gdp-growth", style={"flex": "1 1 45%"}),

    ],
    style={"padding": "1rem"},
)


@app.callback(
    Output("gdp-growth", "figure"),
    Input("country-dropdown", "value"),
)
def update_graph(selected_country: str):
    filtered = df[df["country"] == selected_country]

    fig_gdp = px.line(
        filtered,
        x="year",
        y="gdpPercap",
        markers=True,
        title=f"GDP per Capita in {selected_country}"
    )

    return fig_gdp



# Run the app
if __name__ == "__main__": 
    app.run(debug=True) 
