from dash import Dash

external_stylesheets = 'assets/bootstrap-grid.min.css'

app = Dash(__name__, 
           external_stylesheets=[external_stylesheets])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True