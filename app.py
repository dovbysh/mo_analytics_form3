from dash import Dash

external_stylesheets = 'assets/bootstrap-grid.min.css'

app = Dash(__name__, external_stylesheets=[external_stylesheets])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

# add server health check
@app.server.route("/health")
def check_health():
    return "{status: ok}"

# add server readiness check
@app.server.route("/readiness")
def check_readiness():
    return "{status: ok}"