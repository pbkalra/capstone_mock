
from flask import Flask, render_template, request, redirect
import networkx as nx

app = Flask(__name__)

app.vars = dict()
import pandas as pd
author_df = pd.read_csv('small_authors2.csv', encoding='utf-8')
#mygraph = nx.read_gml('small_authors.gml')
#nx.read_adjlist('social_sublist.edgelist')
#mygraph = nx.DiGraph(nx.read_edgelist('small_authors.edgelist', encoding='utf-8'))
with open('myedgelist_lines.txt', 'r') as filehandle:
	myedgelist = [current_place.rstrip(', ').rstrip() for current_place in filehandle.readlines()]
list_of_tuples = list()
for i in range(len(myedgelist)):
	list_of_tuples.append(tuple(myedgelist[i].strip().split(',')[:2]))

mygraph = nx.DiGraph()
mygraph.add_edges_from(list_of_tuples)


@app.route('/', methods =['GET', 'POST'])
def index():
	if  request.method == 'GET':
		return render_template('info.html')
	elif request.method == 'POST':
		app.vars['name'] = request.form['name']
		print(app.vars)

@app.route('/graph', methods = ['GET', 'POST'])
def graph():
	if request.method=='GET':
		return render_template('interactive_graphs.html')

@app.route('/userinfo', methods = ['GET', 'POST'])
def userinfo():
	if request.method=='GET':
		return render_template('userinfo.html')

def find_authors(area, method):
    c1 = author_df[area]==0 
    c2 = author_df[method]==0
    out = author_df[c1 & c2]
    out2 = out.sort_values('count', ascending=False)
    out3 = out2.keynames[:3]
    return list(out3)


@app.route('/about2', methods = ['GET', 'POST'])
def about2():
	app.vars['name'] = request.form['name_lulu']
	app.vars['yf'] = request.form['source_field']
	app.vars['yf2'] = request.form['source_field2']
	app.vars['cf'] = request.form['destination_field'] 
	app.vars['ra'] = request.form['topic']
	source_nodes = find_authors(app.vars['yf'], app.vars['yf2'])
	target_nodes = find_authors(app.vars['cf'], app.vars['ra'])
	if not source_nodes:
		source_nodes = [1, 2, 3]
	if not target_nodes:
		target_nodes = [4,5,6]
	app.vars['source_nodes'] = source_nodes
	app.vars['target_nodes'] = target_nodes
	app.vars['R1'] = source_nodes[0]
	app.vars['R2'] = source_nodes[1]
	app.vars['R3'] = source_nodes[2]
	try:
		return render_template('about3.html', name=app.vars['name'], cf=app.vars['cf'], ra=app.vars['ra'],  myR1=app.vars['source_nodes'][0], myR2=app.vars['source_nodes'][1], myR3=app.vars['R1'], myC1=target_nodes[0], myC2=target_nodes[1], myC3=target_nodes[2])
	except KeyError:
		print('KeyError')
		return render_template('about3.html', name = 'no name')
	
	
 
	
	


def findpath(graph, x,y):
	try: 
        	path = nx.shortest_path(graph, source=x, target=y)
        #print('You are connected to', y, ' within ', len(path), 'degrees')
        #print(path)
        	return path
	except nx.exception.NetworkXNoPath: 
		path = 'There is no direct path--try cold calling!'
		return path



@app.route('/results', methods = ['GET', 'POST'])
def results():
	if request.method=='POST':	
		print(request.form.keys)
		app.vars['start_node'] = request.form['start_node']
		app.vars['target_node'] = request.form['target_node']
		target1 = 'Booth_JR'
		mypath = findpath(mygraph, app.vars['start_node'], app.vars['target_node'])	
		try:
			return render_template('results.html', out_1 = app.vars['target_node'], mypath = mypath, num_nodes = len(mypath))
		except KeyError:
			return render_template('results.html', out_1 = target1, mypath = mypath, num_nodes = "Oops: key error")
		except TypeError:
			return render_template('results.html', out_1 = target1, mypath = target, num_nodes = ("Oops: type error", source1))
		
	elif request.method=='GET':
		return(render_template('results.html', out_1='BOOTH_JR', mypath='GET', num_nodes = 'GET'))


if __name__ == '__main__':
	app.run(port=8000, debug=True)
