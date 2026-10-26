from flask import render_template, flash, redirect
from app.source.web import server

@server.route('/add-food', methods=['GET', 'POST'])
def add_food_route():
	if request.method == 'GET':
		return render_template('add-food.html')

	food = request.form['nombre']
	prep_time = request.form['tiempo_preparacion']
	cook_time = request.form['tiempo_coccion']

	connection = connect()
	cursor = connection.cursor()
	cursor.execute(
		'insert into comidas(nombre, tiempo_preparacion, tiempo_coccion) values (%s, %s, %s)',
		(food, prep_time, cook_time)
	)

	connection.commit()

	flash('Comida agregada correctamente')

	cursor.close()
	connection.close()

	return redirect(url_for('menu'))
