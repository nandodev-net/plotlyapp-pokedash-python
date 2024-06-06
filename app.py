import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

"""
Load the dataset and initialize the Dash application.

Attributes:
    df (DataFrame): DataFrame containing Pokémon data loaded from CSV file.
    app (Dash): Dash application instance.
"""
df = pd.read_csv("data/pokemon.csv")

app = Dash(__name__)

"""
Define the layout of the Dash application.

Components:
    html.H1: Title of the dashboard.
    dcc.Dropdown: Dropdown for selecting Pokémon type.
    dcc.Dropdown: Dropdown for selecting metric to display.
    dcc.Dropdown: Dropdown for selecting chart type.
    dcc.Graph: Graph component to display the selected chart.
"""
app.layout = html.Div(
    [
        html.Div(
            [
            html.Img(src='/assets/img/banner.jpg', className='blurry-image'),
            html.Img(src='/assets/img/pokedash.png', className='title'),
            ]
        ),
        html.H1(className='space'),
        html.P(children="select your Pokemon type:"),
        dcc.Dropdown(
            id="dropdown-type-selection",
            options=[{"label": type_, "value": type_} for type_ in df.type.unique()],
            value="Grass",
        ),
        html.P(children="select your Pokemon stat:"),
        dcc.Dropdown(
            id="dropdown-metric-selection",
            options=[
                {"label": "HP", "value": "hp"},
                {"label": "Attack", "value": "attack"},
                {"label": "Defense", "value": "defense"},
                {"label": "Speed", "value": "speed"},
                {"label": "Special Attack", "value": "sp_attack"},
                {"label": "Special Defense", "value": "sp_defense"},
                {"label": "Total", "value": "total"},
            ],
            value="hp",
        ),
        html.P(children="select your chart type:"),
        dcc.Dropdown(
            id="dropdown-chart-type",
            options=[
                {"label": "Bar", "value": "bar"},
                {"label": "Line", "value": "line"},
                {"label": "Scatter", "value": "scatter"},
                {"label": "Histogram", "value": "histogram"},
                {"label": "Box", "value": "box"},
                {"label": "Violin", "value": "violin"},
                {"label": "Pie", "value": "pie"},
                {"label": "Sunburst", "value": "sunburst"},
                {"label": "Treemap", "value": "treemap"},
                {"label": "Heatmap", "value": "heatmap"},
                {"label": "Density Contour", "value": "density_contour"},
                {"label": "Area", "value": "area"},
                {"label": "Funnel", "value": "funnel"},
                {"label": "Polar Line", "value": "line_polar"},
                {"label": "Polar Scatter", "value": "scatter_polar"},
                {"label": "Polar Bar", "value": "bar_polar"},
            ],
            value="bar",
        ),
        dcc.Graph(id="graph-content"),
    ]
)

"""
Dictionary mapping chart types to Plotly Express functions.

Keys:
    str: Chart type name.
Values:
    function: Corresponding Plotly Express function.
"""
chart_functions = {
    "bar": px.bar,
    "line": px.line,
    "scatter": px.scatter,
    "histogram": px.histogram,
    "box": px.box,
    "violin": px.violin,
    "pie": px.pie,
    "sunburst": px.sunburst,
    "treemap": px.treemap,
    "heatmap": px.density_heatmap,
    "density_contour": px.density_contour,
    "area": px.area,
    "funnel": px.funnel,
    "line_polar": px.line_polar,
    "scatter_polar": px.scatter_polar,
    "bar_polar": px.bar_polar,
}


@callback(
    Output("graph-content", "figure"),
    [
        Input("dropdown-type-selection", "value"),
        Input("dropdown-metric-selection", "value"),
        Input("dropdown-chart-type", "value"),
    ],
)
def update_graph(selected_type, selected_metric, chart_type):
    """
    Callback function to update the graph based on user selections.

    Args:
        selected_type (str): Selected Pokémon type from the dropdown.
        selected_metric (str): Selected metric to display on the y-axis.
        chart_type (str): Selected type of chart to display.

    Returns:
        Figure: Plotly figure object representing the selected chart.

    Description:
        The function filters the DataFrame based on the selected Pokémon type,
        determines the appropriate Plotly Express function to call based on the selected
        chart type, and generates the corresponding chart. The chart is then returned
        to be displayed in the Graph component.
    """
    if selected_type is None:
        selected_type = df['type'].unique()[0]
    if selected_metric is None:
        selected_metric = 'hp'
    if chart_type is None:
        chart_type = 'bar'

    dff = df[df.type == selected_type]
    chart_function = chart_functions[chart_type]

    if chart_type in ["pie", "sunburst", "treemap"]:
        fig = chart_function(
            dff,
            names="name",
            values=selected_metric,
            title=f"{selected_metric.capitalize()} of {selected_type} Type Pokémon",
        )
    elif chart_type in ["line_polar", "scatter_polar", "bar_polar"]:
        fig = chart_function(
            dff,
            r=selected_metric,
            theta="name",
            title=f"{selected_metric.capitalize()} of {selected_type} Type Pokémon",
        )
    else:
        fig = chart_function(
            dff,
            x="name",
            y=selected_metric,
            title=f"{selected_metric.capitalize()} of {selected_type} Type Pokémon",
        )

    return fig


if __name__ == "__main__":
    """
    Run the Dash application.

    Args:
        debug (bool): If True, enable debug mode.

    Description:
        This block checks if the script is run directly (not imported as a module),
        and if so, runs the Dash application with debug mode enabled.
    """
    app.run(debug=True)
