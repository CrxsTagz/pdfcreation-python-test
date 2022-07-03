import dash
import dash_html_components as html
from PDF_creation import getpdf

app = dash.Dash(__name__)

app.layout = html.Div(children=[
                       html.Div([            
                       html.Button('pdf', id='pdf-button', n_clicks=0),
                       html.Div(id='output-container-button', children='Hit the button to create a pdf')
                      ])
                ])                      
                
@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('apply-button', 'n_clicks')])
def run_script_onClick(n_clicks):
    #print('[DEBUG] n_clicks:', n_clicks)
    
    if not n_clicks:
        #raise dash.exceptions.PreventUpdate
        return dash.no_update

    # without `shell` it needs list ['/full/path/python', 'script.py']           
    #result = subprocess.check_output( ['/usr/bin/python', 'script.py'] )  

    # with `shell` it needs string 'python script.py'
    #  subprocess.check_output('python script.py', shell=True)  
    result = getpdf
    # convert bytes to string
    result = result.decode()  
    
    return result
            
if __name__ == "__main__":
    app.run_server(port=8080, debug=True)