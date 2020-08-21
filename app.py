from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.vars = dict()

@app.route('/', methods =['GET', 'POST'])
def index():
	if  request.method == 'GET':
		return render_template('userinfo.html')
	elif request.method == 'POST':
		app.vars['name'] = request.form['name']
		print(app.vars)

@app.route('/about', methods = ['GET', 'POST'])
def about():
  	try:
		return render_template('about.html', name = request.form['name_lulu'], yf = request.form['source_field'], cf = request.form['destination_field'], ra = request.form['topic'])
	except KeyError:
		return render_template('about.html', name = 'ooga booga')
if __name__ == '__main__':
  app.run(port=33507)
