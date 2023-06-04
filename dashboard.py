import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load the data
df = pd.read_csv('internet_usage_clean.csv')
# Load country-continent mapping
country_continent = pd.read_csv('country_continent.csv')
# Merge the dataframes
df = pd.merge(df, country_continent, on='Country', how='left')
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
    html.Div([
        dcc.Graph(id='world-map', style={"height" : "800px", "width": "65%"}),
        dcc.Graph(id='continent-bar', style={"width": "35%"})
    ], style={'display': 'flex', 'width': '100%'})
])

# Define the callback to update the map based on the selected year
@app.callback(
    [Output('world-map', 'figure'), Output('continent-bar','figure')],
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
    df_continent = df_year.groupby('Continent')[str(selected_year)].mean().reset_index()
    fig_bar = px.bar(
        df_continent,
        x='Continent',
        y=str(selected_year),
        title=f'Average Internet Usage by Continent in {selected_year}',
        labels={str(selected_year): 'Average Usage'},
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    return fig_map, fig_bar

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)