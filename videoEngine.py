import json
import dash
import urllib
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app_colors = {
  'background': '#0C0F0A',
  'text': '#FFFFFF',
  'someothercolor':'#CF0009',
}

app.layout = html.Div([
	html.Hr(),
	html.Div([
		html.Div([
			html.H4('YouTube')
		], style={'textAlign' : 'right', 'color' : app_colors['text']},
		className='three columns'),
		html.Div([
			dcc.Input(id='search_query', value='',
				type='text', size=60,
				placeholder='Search videos online: ')
		], className='six columns'),
		html.Div([
			html.H4('Unofficial site')
		], style={'textAlign' : 'left', 'color' : app_colors['text']},
		className='three columns')
	], className='row'),
	html.Hr(),
	html.Div(id='output-container')
], style={'backgroundColor' : app_colors['background']})

def search_YouTube(query):
	with open('youtube_api.txt', 'r') as yk:
		key = yk.read()

	youtube_link = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults='+str(15)+'&q='+str(query)+'&safeSearch=moderate&key='+str(key)

	response = urllib.urlopen(youtube_link).read()
	search_list = json.loads(response)

	titles = []
	descriptions = []
	video_links = []

	for search_items in search_list['items']:
		for snip, snip_val in search_items['snippet'].items():
			if snip == 'title':
				titles.append(snip_val)
			if snip == 'description':
				descriptions.append(snip_val)

		for ids, id_value in search_items['id'].items():
			if ids == 'videoId':
				video_links.append('https://www.youtube.com/watch?v=' + str(id_value))
			if ids == 'playlistId':
				video_links.append(str(id_value))

	whole_bunch = zip(titles, descriptions, video_links)
	for tdl in whole_bunch:
		if not tdl[2].startswith('https'):
			whole_bunch.remove(tdl)

	return whole_bunch

@app.callback(
	Output('output-container', 'children'),
	[Input('search_query', 'value')]
)

def get_search_list(query):
	whole_bunch = search_YouTube(query)
	streaming = []
	try:
		for stream in whole_bunch:
			streaming.append(
				html.Div([
			 		html.H6(stream[0], style={'color' : app_colors['text']}),
			 		html.P(stream[1], style={'color' : app_colors['text']}),
			 		html.A(html.Button('YouTube Video', style={'color' : app_colors['someothercolor']}, 
			 			className='three columns'), href=stream[2], target='blank'),
			 		html.P('---' * 68)
			 	], className='container')
			)
		return streaming
	except Exception as e:
		return html.Div([
			html.P('Request cannot be processed.'),
			html.P('Please give valid Input.')
		], className='container', style={'textAlign' : 'center'})

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)