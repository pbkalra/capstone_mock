
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.vars = dict()

import random


import networkx as nx
with open('small_net_edgelines.txt', 'r') as filehandle:
	myedgelist = [current_place.rstrip(', ').rstrip() for current_place in filehandle.readlines()]
list_of_tuples = list()
for i in range(len(myedgelist)):
	list_of_tuples.append(tuple(myedgelist[i].strip().split(',')[:2]))

mygraph = nx.DiGraph()
mygraph.add_edges_from(list_of_tuples)

poplist2 = ['Ana Oliveira',
 'Ann Van Ness',
 'Audrey Gruss',
 'Chele Chiavacci',
 'Christine Schott',
 'Cole Rumbough',
 'Diana Taylor',
 'Eleanora Kennedy',
 'Felicia Taylor',
 'Geoffrey Bradfield',
 'Janna Bullock',
 'Katlean de Monchy',
 'Lucia Hwong Gordon',
 'Martin Shafiroff',
 'Muffie Potter Aston',
 'Sharon Bush',
 'Sharon Kerr',
 'Patricia Shiah',
 'Somers Farkas',
 'Yaz Hernandez']


def findpath(graph, x,y):
	try: 
        	path = nx.shortest_path(graph, source=x, target=y)
        #print('You are connected to', y, ' within ', len(path), 'degrees')
        #print(path)
        	return path
	except nx.exception.NetworkXNoPath: 
	        path = 'There is no direct path--try cold calling!'
		return path



@app.route('/', methods =['GET', 'POST'])
def index():
	if  request.method == 'GET':
		return render_template('userinfo.html')
	elif request.method == 'POST':
		app.vars['name'] = request.form['name']
		print(app.vars)


@app.route('/about2', methods = ['GET', 'POST'])
def about2():
	try:
		return render_template('about2.html', name = request.form['name_lulu'], yf = request.form['source_field'], cf = request.form['destination_field'], ra = request.form['topic'])
	except KeyError:
		return render_template('about2.html', name = 'no name')

@app.route('/results', methods = ['GET', 'POST'])
def results():
	start_point = 'Muffie Potter Aston' #request.form['R1']
	tnum = random.randint(0,19)
	snum = random.randint(0,19)
	start_point = poplist2[snum]
	target1 = poplist2[tnum]
	source1 = start_point
	mypath = findpath(mygraph, start_point, target1)
	try:
		return render_template('results.html', out_1 = target1, mypath = mypath, num_nodes = len(mypath))
	except KeyError:
		return render_template('results.html', out_1 = source1, mypath = mypath, num_nodes = "Oops: key error")
	except TypeError:
		return render_template('results.html', out_1 = source1, mypath = target, num_nodes = ("Oops: type error", source1))

if __name__ == '__main__':
	app.run(port=33507)
