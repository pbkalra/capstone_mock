from flask import Flask, render_template, request, redirect
import networkx as nx

app = Flask(__name__)

app.vars = dict()
import pandas as pd
author_df = pd.read_csv('small_authorsFri5.csv', encoding="utf-8")
author_df = author_df.set_index(['dictkey'])


#mygraph = nx.read_gml('small_authors.gml')
#nx.read_adjlist('social_sublist.edgelist')
#mygraph = nx.DiGraph(nx.read_edgelist('small_authors.edgelist', encoding='utf-8'))
with open('myedgelist_linesFri5.txt', 'r') as filehandle:
	myedgelist = [current_place.rstrip(', ').strip() for current_place in filehandle.readlines()]
list_of_tuples = list()
for i in range(len(myedgelist)):
	list_of_tuples.append(tuple(myedgelist[i].strip(',').split(', ')[:2]))

mygraph = nx.Graph()
mygraph.add_edges_from(list_of_tuples)


@app.route('/')
def index():
	return render_template('info.html')
	

@app.route('/graph')
def graph():
	return render_template('interactive_graphs2.html')

@app.route('/userinfo', methods = ['GET', 'POST'])
def userinfo():
	if request.method=='GET':
		return render_template('userinfo.html')
	#elif request.method=='POST':
	

def find_authors(area, method):
    c1 = (author_df['primary_area']==area)
    c2 = (author_df['primary_method']==method)
    out = author_df[c1 & c2]
    out2 = out.sort_values('count', ascending=False)
    out3 = out2.index[:3]
    return out3

@app.route('/about2', methods = ['GET', 'POST'])
def about2():
	name = request.form['name']
	app.vars['yf'] = request.form['source_field']
	app.vars['yf2'] = request.form['source_field2']
	app.vars['cf'] = request.form['destination_field'] 
	app.vars['ra'] = request.form['topic']


	source_nodes_idx = list(find_authors(app.vars['yf'], app.vars['yf2']))
	target_nodes_idx = list(find_authors(app.vars['cf'], app.vars['ra']))
	if len(source_nodes_idx)==0:
		source_nodes_idx = ['coch_d', 'bunge_s', 'gabrieli_j']
	elif len(source_nodes_idx)<3:
		source_nodes_idx.extend(['bunge_s', 'gabrieli_j'])
	if len(target_nodes_idx)==0:
		target_nodes_idx = ['coch_d', 'bunge_s', 'gabrieli_j']
	elif len(target_nodes_idx)<3:
		target_nodes_idx.extend(['bunge_s', 'gabrieli_j'])

	app.vars['R1_name'] = (author_df.loc[source_nodes_idx[0],'first_name'] + ' ' + author_df.loc[source_nodes_idx[0],'last_name']) 
	app.vars['R2_name'] = (author_df.loc[source_nodes_idx[1],'first_name'] + ' ' + author_df.loc[source_nodes_idx[1],'last_name'])
	app.vars['R3_name'] = (author_df.loc[source_nodes_idx[2],'first_name'] + ' ' + author_df.loc[source_nodes_idx[2],'last_name'])

	app.vars['C1_name'] = (author_df.loc[target_nodes_idx[0],'first_name'] + ' ' + author_df.loc[target_nodes_idx[0],'last_name']) 
	app.vars['C2_name'] = (author_df.loc[target_nodes_idx[1],'first_name'] + ' ' + author_df.loc[target_nodes_idx[1],'last_name'])
	app.vars['C3_name'] = (author_df.loc[target_nodes_idx[2],'first_name'] + ' ' + author_df.loc[target_nodes_idx[2],'last_name'])	

	app.vars['R1_value'] = (source_nodes_idx[0]) 
	app.vars['R2_value'] = (source_nodes_idx[1])
	app.vars['R3_value'] = (source_nodes_idx[2])

	app.vars['C1_value'] = (target_nodes_idx[0])
	app.vars['C2_value'] = (target_nodes_idx[1])
	app.vars['C3_value'] = (target_nodes_idx[2])

	try:
		return render_template('about3.html', name=name, cf=app.vars['cf'], ra=app.vars['ra'],  
		myR1=app.vars['R1_name'], myR2=app.vars['R2_name'], myR3=app.vars['R3_name'], 
		myC1=app.vars['C1_name'], myC2=app.vars['C2_name'], myC3=app.vars['C3_name'], 
		R1value = app.vars['R1_value'], R2value = app.vars['R2_value'], R3value = app.vars['R3_value'],
		C1value = app.vars['C1_value'], C2value = app.vars['C2_value'], C3value = app.vars['C3_value'] )		
		print(app.vars)

	except KeyError:
		print('KeyError')
		return render_template('about3.html', name = 'no name')
		print(app.vars)

def findpath(graph, x,y):
	try: 
        	path = nx.shortest_path(graph, source=x, target=y)
        	return path
	except nx.exception.NetworkXNoPath: 
		path = 'There is no direct path--try cold calling!'
		return path


@app.route('/results', methods = ['GET', 'POST'])
def results():
	if request.method=='POST':	
		#print(request.form.keys())
		start_node = str(request.form['start_node'])
		target_node = str(request.form['target_node'])
		target1 = 'Booth_JR'
		target_name = author_df.at[target_node, 'first_name'] + ' ' + author_df.at[target_node,'last_name']
		mypath_raw = findpath(mygraph, start_node, target_node)	
		mypath_finished = list()
		for auth in mypath_raw:
			mypath_finished.append(str(author_df.at[auth, 'first_name'] + ' ' + author_df.at[auth,'last_name']) )


		try:
			return render_template('results.html', out_1 = target_name, mypath = mypath_finished, num_nodes = len(mypath_raw))
		except KeyError:
			return render_template('results.html', out_1 = target1, mypath = mypath_finished, num_nodes = "Oops: key error")
		except TypeError:
			return render_template('results.html', out_1 = target1, mypath = target, num_nodes = ("Oops: type error", source1))

	elif request.method=='GET':
		return(render_template('results.html', out_1='BOOTH_JR', mypath='GET', num_nodes = 'GET'))


if __name__ == '__main__':
	app.run(port=8000, debug=True)
