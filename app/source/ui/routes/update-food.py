@app.route('/update_comida/<int:id>', methods=['GET', 'POST'])
def update_comida(id):
	connection = connect()
	cursor = connection.cursor()
	
	if request.method == 'POST':
		comida = request.form['nombre']
		tiempo_preparacion = request.form['tiempo_preparacion']
		tiempo_coccion = request.form['tiempo_coccion']
		try:
			cursor.execute(
				'UPDATE comidas SET nombre = %s, tiempo_preparacion = %s, tiempo_coccion = %s WHERE id = %s',
				(comida, tiempo_preparacion, tiempo_coccion, id))
			connection.commit()
			flash('Comida actualizada correctamente')
		except Exception as e:
			connection.rollback()
			flash(f'Error al actualizar comida: {e}')
		finally:
			cursor.close()
			connection.close()
		return redirect(url_for('menu'))
	
	try:
		cursor.execute('SELECT * FROM comidas WHERE id = %s', (id,))
		item = cursor.fetchone()
	except Exception as e:
		return f"Error de conexión con la base de data: {e}"
	finally:
		cursor.close()
		connection.close()
		
	return render_template('update_comida.html', item=item)
