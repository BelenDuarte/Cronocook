@server.route('/delete_comida/<int:id>', methods=['POST'])
def delete_food_route(id):
	connection = connect()
	cursor = connection.cursor()
	try:
		cursor.execute('DELETE FROM comidas WHERE id = %s', (id,))
		connection.commit()
		flash('Comida eliminada correctamente')
	except Exception as e:
		connection.rollback()
		flash(f'Error al eliminar comida: {e}')
	finally:
		cursor.close()
		connection.close()
	return redirect(url_for('menu'))
