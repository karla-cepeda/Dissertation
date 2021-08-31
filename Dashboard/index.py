import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import server
from app import app
from apps import home, dashboard

dash.Dash(__name__)

# Menu for access to different pages.
navbar = dbc.Nav(
                [
                    dbc.NavLink(children=["Home"], href="/home",  active='exact', id="homeid", style={'color':'white'}, className='danger'),
                    dbc.NavLink(children=["Dashboard"], href="/dashboard",  active='exact', style={'color':'white'}, className='danger'),
                ],
                vertical=False,
                className = 'danger',
            )
    
upperbar = html.Nav(
                [
                    html.A("Sentiment Project", className="navbar-brand col-sm-3 col-md-2 mr-0"),
                    html.P(""),
                    navbar
                ],
                className = "navbar navbar-dark sticky-top bg-danger flex-md-nowrap p-0",
            )

# Content where other pages would be drawn.

# Index layout
app.layout = html.Div([dcc.Location(id="url"), 
                       upperbar, 
                       html.Div(
                         html.Div(id="page-content", className="row"), 
                         className = 'container-fluid'
                       )
             ])
                      

@app.callback(
        [Output("page-content", "children"), Output("homeid", "active")], 
        [Input("url", "pathname"),]
    )
def render_page_content(pathname):
    
    pathname = pathname.lower()
    if pathname == "/dashboard":
        
        content = html.Div(dashboard.layout, className = "col-md-9 ml-sm-auto col-lg-10 pt-3 px-4")        
        bodynavbar = html.Div(
                            html.Div(dashboard.filters, className = "sidebar-sticky", style={'padding-left':'10px'}), 
                            className = "col-md-2 d-none d-md-block bg-light sidebar")        

        return [[bodynavbar, content], "exact"]
        
    else:
        content = html.Div(home.layout, className = "col-auto m-auto")        
        
        return [content, True]


if __name__ == '__main__':
    #app.run_server(port=8060, debug=True)
    app.run_server(debug=False)
