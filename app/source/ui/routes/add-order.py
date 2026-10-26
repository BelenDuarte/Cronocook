from app.source.web import server
from app.source.database import connect

@server.route('/add-order', methods=['GET', 'POST'])
def add_order_route():
	connection = connect()
	cursor = connection.cursor()

	cursor.execute('select * from comidas')
	foods = cursor.fetchall()

	if request.method == 'GET':
		cursor.close()
		connection.close()

		return render_template('add-order.html', foods=foods)

	cursor.execute('insert into pedidos() values ()',)
	order_id = cursor.lastrowid

	for field, value in request.form.items():
		if field.startswith('cantidad_'):
			food_id = field.split('_')[1]
			quantity = int(value)

			if quantity > 0:
				cursor.execute(
					'insert into pedidos_detalles(id_pedido, id_comida, cantidad) values (%s, %s, %s)',
					(order_id, food_id, quantity)
				)

	connection.commit()

	flash('Pedido agregado correctamente')

	cursor.close()
	connection.close()

	return redirect(url_for('orders'))
