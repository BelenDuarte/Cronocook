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

#Sitio web principal
@app.route('/')
def index():
    return render_template('index.html')

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
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                'INSERT INTO comidas(nombre, tiempo_preparacion, tiempo_coccion) VALUES (%s, %s, %s)',
                (comida, tiempo_preparacion, tiempo_coccion))
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
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                'UPDATE comidas SET nombre = %s, tiempo_preparacion = %s, tiempo_coccion = %s WHERE id = %s',
                (comida, tiempo_preparacion, tiempo_coccion, id))
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

#------------------------------ seccion de pedidos ----------------------------------------------------------
#pagina que muestra los pedidos
@app.route('/pedidos')
def pedidos():
    try:
        cur = mysql.connection.cursor()

        # Trae id y fecha de cada pedido.
        cur.execute('SELECT * FROM pedidos')
        datos = cur.fetchall()

        # Trae los ítems de TODOS los pedidos, con el nombre
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

    except Exception as e:
        return f"Error de conexión con la base de datos: ¿Está prendido el servidor MySQL en XAMPP? {e}"

    return render_template('pedidos.html', pedidos=datos, pedidos_agrupados=pedidos_agrupados)

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
    
    return render_template('tiempo_espera.html')
#--------------------------- hasta aca llegaste porfa no escribas nada mas si no viste en clase ---------------------------
# ------------------------------------------------- enserio porfa -----------------------------------------------
# Ruta nueva que muestra los proyectos

if __name__== "__main__":
    app.run(debug=True, host = '0.0.0.0')