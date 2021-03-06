import dash
import dash_bootstrap_components as dbc

# bootstrap theme
# https://bootswatch.com/lux/
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.LITERA],)

app.title = "Sentment Analysis on COVID-19 vaccines in Ireland"

server = app.server
app.config.suppress_callback_exceptions = True

