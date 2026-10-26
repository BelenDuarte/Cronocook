from app.source.database import connect
from app.source.web import server
from flask import render_template

@server.route('/menu')
def menu_route():
	connection = connect()
	cursor = connection.cursor()
	cursor.execute('select * from comidas')
	data = cursor.fetchall()
	cursor.close()
	connection.close()

	return render_template('menu.html', foods=data)
