import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dashapp import application
from flask_login import login_required
from flask import session


do_something = 'Demo'


demo_app = dash.Dash(__name__, server = application, routes_pathname_prefix = '/demo_app/', assets_folder = 'static', assets_url_path = '/static')
demo_app.scripts.config.serve_locally = True
demo_app.css.config.serve_locally = True
demo_app.title = 'Savanta'

demo_app.layout = html.Div(
	className = 'xcontainer',
	children = [
	
		#Header
		html.Div(
			id = 'header',
			className = 'header',
			children = [
				
				html.Div(
					className = 'logins',
					children = [
						html.Div(id = 'user', style = {'margin-right': '20px'}),
						html.A(id = 'home', style = {'margin-right': '10px'}, href = '/home', children = 'Home'),
						html.A(id = 'logout', href = '/logout', children = 'Logout'),
				]),
		]),
		
		#Main
		html.Div(
			id = 'main',
			className = 'main',
			children = [
				do_something
		]),

])

#Callbacks

@demo_app.callback(
	Output('user', 'children'),
	[Input('logout', 'children')])
def update_user(children):
	return 'User: {}'.format(session.get('username', None))

for view_func in demo_app.server.view_functions:
	if view_func.startswith('/demo_app/'):
		demo_app.server.view_functions[view_func] = login_required(demo_app.server.view_functions[view_func])
