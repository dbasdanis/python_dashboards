import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load the data
df = pd.read_csv('internet_usage_clean.csv')
# Extract unique years from the dataframe
years = [col for col in df.columns if col.isdigit()]
# Initialize the Dash app
app = dash.Dash(__name__)
# Define the layout
app.layout = html.Div([
    html.H6("Select Year:"),
    dcc.Slider(
        id='year-slider',
        min=int(years[0]),
        max=int(years[-1]),
        value=int(years[0]),
        marks={str(year): str(year) for year in years},
        step=None
    ),
    dcc.Graph(id='world-map', style={"height" : "800px", "width": "100%"})
])

# Define the callback to update the map based on the selected year
@app.callback(
    Output('world-map', 'figure'),
    [Input('year-slider', 'value')]
)
def update_map(selected_year):
    df_year = df[['Country', str(selected_year)]].dropna()
    fig_map = px.choropleth(
        df_year,
        locations='Country',
        locationmode='country names',
        color=str(selected_year),
        hover_name='Country',
        projection='natural earth',
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f'Global Internet Usage in {selected_year}'
    )
    fig_map.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
    fig_map.update_layout(height=800, geo=dict(scope='world', projection_scale=1))
    return fig_map

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)