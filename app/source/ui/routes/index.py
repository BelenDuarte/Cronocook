from app.source.web import server
from flask import render_template

@server.route('/')
def index_route():
	return render_template('index.html')
