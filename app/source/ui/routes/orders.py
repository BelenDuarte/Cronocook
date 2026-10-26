from app.source.database import connect
from app.source.web import server

@server.route('/orders')
def orders_route():
	connection = connect()
	cursor = connection.cursor()

	cursor.execute('select * from pedidos')
	data = cursor.fetchall()

	cursor.execute('''
		select pedidos_detalles.id_pedido, comidas.nombre, pedidos_detalles.cantidad
		from pedidos_detalles
		join comidas on pedidos_detalles.id_comida = comidas.id
	''')

	items = cursor.fetchall()

	cursor.close()
	connection.close()

	orders = {}

	for id_pedido, nombre_comida, cantidad in items:
		orders.setdefault(id_pedido, []).append((nombre_comida, cantidad))

	return render_template('orders.html', pedidos=data, orders=orders)
