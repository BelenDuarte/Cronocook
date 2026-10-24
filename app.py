from flask import Flask, render_template , request , redirect, url_for , flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#-------------------- desde aca podes comenzar a poner cosas ------------------------
app.secret_key = "a_secure_random_key"
#configuracion pr la base de datos MYSQL
app.config ['MYSQL_USER'] = 'root'                            #es admin tiene todos los permisos
app.config ['MYSQL_PASSWORD'] = ''                            #es la contra de ese user
app.config ['MYSQL_HOST'] = '127.0.0.1'                        #local host
app.config ['MYSQL_DB'] = 'burguer'                            #nombre de la base de daos

mysql= MySQL(app)                                             #guardas en un vriable esa base de datos

def obtener_config_turno(cur):
    try:
        cur.execute('SELECT cocineros_coccion, cocineros_preparacion, pedidos_por_cocinero FROM configuracion_turno WHERE id = 1')
        row = cur.fetchone()
        if not row:
            cur.execute('INSERT INTO configuracion_turno (id, cocineros_coccion, cocineros_preparacion, pedidos_por_cocinero) VALUES (1, 3, 3, 2)')
            mysql.connection.commit()
            return {'cocineros_coccion': 3, 'cocineros_preparacion': 3, 'pedidos_por_cocinero': 2, 'cap_coccion': 6, 'cap_preparacion': 6}
        c_coc, c_prep, p_x_c = row
        return {
            'cocineros_coccion': c_coc,
            'cocineros_preparacion': c_prep,
            'pedidos_por_cocinero': p_x_c,
            'cap_coccion': c_coc * p_x_c,
            'cap_preparacion': c_prep * p_x_c
        }
    except Exception as e:
        return {'cocineros_coccion': 3, 'cocineros_preparacion': 3, 'pedidos_por_cocinero': 2, 'cap_coccion': 6, 'cap_preparacion': 6}

#Sitio web principal
@app.route('/')
def index():
    config = {'cocineros_coccion': 3, 'cocineros_preparacion': 3, 'pedidos_por_cocinero': 2, 'cap_coccion': 6, 'cap_preparacion': 6}
    try:
        cur = mysql.connection.cursor()
        config = obtener_config_turno(cur)
        cur.close()
    except Exception as e:
        pass
    return render_template('index.html', config=config)

#-----------------------------todo lo de menu, agregar comida, eliminar comida y actualizar comida------

#pagina que muestra el menu de comidas
@app.route('/menu')
def menu():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM comidas')
        datos = cur.fetchall()
        cur.close()
    except Exception as e:
        return f"Error de conexión con la base de datos: ¿Está prendido el servidor MySQL en XAMPP? {e}"# muestra un mensaje por si no prendi el server
    return render_template('menu.html',menu=datos) 

#Pagina para agregar una comida
@app.route('/add_comida', methods=['GET', 'POST'])
def add_comida():
    if request.method == 'POST':
        comida = request.form['nombre']
        tiempo_preparacion = request.form['tiempo_preparacion']
        tiempo_coccion = request.form['tiempo_coccion']
        url_imagen = request.form['url_imagen']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                'INSERT INTO comidas(nombre, tiempo_preparacion, tiempo_coccion, url_imagen) VALUES (%s, %s, %s, %s)',
                (comida, tiempo_preparacion, tiempo_coccion, url_imagen))
            mysql.connection.commit()
            cur.close()
            flash('Comida agregada correctamente')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al agregar comida: {e}')
        return redirect(url_for('menu'))
    return render_template('add_comida.html')

#Boton para eliminar una comida
@app.route('/delete_comida/<int:id>', methods=['POST'])
def delete_comida(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM comidas WHERE id = %s', (id,))
        mysql.connection.commit()
        cur.close()
        flash('Comida eliminada correctamente')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar comida: {e}')
    return redirect(url_for('menu'))

#Boton para actualizar una comida
@app.route('/update_comida/<int:id>', methods=['GET', 'POST'])
def update_comida(id):
    if request.method == 'POST':
        comida = request.form['nombre']
        tiempo_preparacion = request.form['tiempo_preparacion']
        tiempo_coccion = request.form['tiempo_coccion']
        url_imagen = request.form['url_imagen']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                'UPDATE comidas SET nombre = %s, tiempo_preparacion = %s, tiempo_coccion = %s, url_imagen = %s WHERE id = %s',
                (comida, tiempo_preparacion, tiempo_coccion, url_imagen, id))
            mysql.connection.commit()
            cur.close()
            flash('Comida actualizada correctamente')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al actualizar comida: {e}')
        return redirect(url_for('menu'))
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM comidas WHERE id = %s', (id,))
        item = cur.fetchone()
        cur.close()
    except Exception as e:
        return f"Error de conexión con la base de datos: {e}"
    return render_template('update_comida.html', item=item)
#----------------------------------------------------------------------------------------------------

#------------------------------ seccion de pedidos y capacidad ----------------------------------------------------------
#pagina que muestra los pedidos filtrados por la capacidad de cocineros
@app.route('/pedidos')
def pedidos():
    try:
        cur = mysql.connection.cursor()

        # 1. Trae la configuración del turno para saber cuántos pedidos entran a la pantalla
        config = obtener_config_turno(cur)
        cap_coccion = config['cap_coccion']

        # 2. Trae los pedidos pendientes (que no han sido finalizados) ordenados por llegada
        cur.execute("SELECT * FROM pedidos WHERE estado != 'finalizado' ORDER BY id ASC")
        datos = cur.fetchall()

        # 3. Trae los ítems de TODOS los pedidos, con el nombre
        # de la comida en vez del id
        cur.execute('''
            SELECT pedidos_detalles.id_pedido, comidas.nombre, pedidos_detalles.cantidad
            FROM pedidos_detalles
            JOIN comidas ON pedidos_detalles.id_comida = comidas.id
        ''')
        items = cur.fetchall()

        cur.close()

        # Agrupación: paso de "lista plana de ítems" a "diccionario por pedido".
        pedidos_agrupados = {}
        for id_pedido, nombre_comida, cantidad in items:
            pedidos_agrupados.setdefault(id_pedido, []).append((nombre_comida, cantidad))

        # 4. REGLA DE CAPACIDAD: Se toman hasta 2 pedidos por cocinero (cap_coccion)
        # Los primeros entran a pantalla activa, los restantes quedan en cola de espera
        pedidos_activos = datos[:cap_coccion]
        pedidos_en_cola = datos[cap_coccion:]

    except Exception as e:
        return f"Error de conexión con la base de datos: ¿Está prendido el servidor MySQL en XAMPP? {e}"

    return render_template(
        'pedidos.html', 
        pedidos=pedidos_activos, 
        pedidos_en_cola=pedidos_en_cola, 
        pedidos_agrupados=pedidos_agrupados,
        config=config,
        slots_ocupados=len(pedidos_activos),
        slots_disponibles=max(0, cap_coccion - len(pedidos_activos))
    )

# Acción para finalizar un pedido y liberar un slot para el siguiente en cola
@app.route('/completar_pedido/<int:id>', methods=['POST'])
def completar_pedido(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE pedidos SET estado = 'finalizado' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        flash(f'Pedido #{id} completado. Se liberó un puesto y entra el siguiente pedido de la cola.')
    except Exception as e:
        flash(f'Error al completar pedido: {e}')
    return redirect(url_for('pedidos'))

# Menú para editar el número de empleados en cocción y preparación
@app.route('/configuracion_turno', methods=['GET', 'POST'])
def configuracion_turno():
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            cocineros_coccion = int(request.form.get('cocineros_coccion', 3))
            cocineros_preparacion = int(request.form.get('cocineros_preparacion', 3))
            pedidos_por_cocinero = int(request.form.get('pedidos_por_cocinero', 2))

            if cocineros_coccion < 1: cocineros_coccion = 1
            if cocineros_preparacion < 1: cocineros_preparacion = 1
            if pedidos_por_cocinero < 1: pedidos_por_cocinero = 1

            cur.execute('''
                UPDATE configuracion_turno 
                SET cocineros_coccion = %s, cocineros_preparacion = %s, pedidos_por_cocinero = %s 
                WHERE id = 1
            ''', (cocineros_coccion, cocineros_preparacion, pedidos_por_cocinero))
            mysql.connection.commit()
            flash('¡Configuración de empleados actualizada! La capacidad de cocina se ha recalculado.')
            cur.close()
            return redirect(url_for('configuracion_turno'))

        config = obtener_config_turno(cur)
        cur.close()
        return render_template('configuracion_turno.html', config=config)
    except Exception as e:
        return f"Error de conexión con la base de datos: {e}"

@app.route('/add_pedido', methods=['GET', 'POST'])
def add_pedido():
    try:
        #si la base esta prendida mostra lo que hay en la tabla comidas
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM comidas')
        comidas = cur.fetchall()
        cur.close()
    #si la base no esta prendida muestra un error
    except Exception as e:
        return f"Error de conexión con la base de datos: {e}"
    
    if request.method == 'POST':
        try:
            # añade a la tabla pedidos un id nuevo y la fecha que se creo
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO pedidos() VALUES ()',)

            # aqui nos vos vamos a la tabla donde guardamos que y cuanto de cada comida
            pedido_id = cur.lastrowid
            for campo, valor in request.form.items():
                if campo.startswith('cantidad_'):
                    id_comida = campo.split('_')[1]
                    cantidad = int(valor)
                    if cantidad > 0:
                        cur.execute(
                            'INSERT INTO pedidos_detalles(id_pedido, id_comida, cantidad) VALUES (%s, %s, %s)',
                            (pedido_id, id_comida, cantidad))

            mysql.connection.commit()
            cur.close()
            flash('Pedido agregado correctamente')
            return redirect(url_for('pedidos'))
        except Exception as e:
            return f"Error de conexión con la base de datos: {e}"

    return render_template('add_pedido.html', comidas=comidas)

@app.route('/tiempo_espera')
def tiempo_espera():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pedidos ORDER BY fecha_pedido DESC')
        pedidos = cur.fetchall()
        cur.close()
    except Exception as e:
        pedidos = []
    return render_template('tiempo_espera.html', pedidos=pedidos)
#--------------------------- hasta aca llegaste porfa no escribas nada mas si no viste en clase ---------------------------
# ------------------------------------------------- enserio porfa -----------------------------------------------
# Ruta nueva que muestra los proyectos

if __name__== "__main__":
    app.run(debug=True, host = '0.0.0.0')