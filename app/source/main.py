from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates', static_folder='../static')

#-------------------- Configuración y Base de Datos ------------------------
app.secret_key = "a_secure_random_key"

# Configuración para la base de datos MySQL (XAMPP)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'burguer'

mysql = MySQL(app)

# Sitio web principal
@app.route('/')
def index():
    return render_template('index.html')

#----------------------------- Menú y CRUD de Comidas ----------------------

@app.route('/menu')
def menu():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM comidas')
        datos = cur.fetchall()
        cur.close()
    except Exception as e:
        return f"Error de conexión con la base de datos: ¿Está prendido el servidor MySQL en XAMPP? {e}"
    return render_template('menu.html', menu=datos) 

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

#------------------------------ Sección de Pedidos ----------------------------------------------------------

@app.route('/pedidos')
def pedidos():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pedidos')
        datos = cur.fetchall()

        cur.execute('''
            SELECT pedidos_detalles.id_pedido, comidas.nombre, pedidos_detalles.cantidad
            FROM pedidos_detalles
            JOIN comidas ON pedidos_detalles.id_comida = comidas.id
        ''')
        items = cur.fetchall()
        cur.close()

        pedidos_agrupados = {}
        for id_pedido, nombre_comida, cantidad in items:
            pedidos_agrupados.setdefault(id_pedido, []).append((nombre_comida, cantidad))

    except Exception as e:
        return f"Error de conexión con la base de datos: ¿Está prendido el servidor MySQL en XAMPP? {e}"

    return render_template('pedidos.html', pedidos=datos, pedidos_agrupados=pedidos_agrupados)

@app.route('/add_pedido', methods=['GET', 'POST'])
def add_pedido():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM comidas')
        comidas = cur.fetchall()
        cur.close()
    except Exception as e:
        return f"Error de conexión con la base de datos: {e}"
    
    if request.method == 'POST':
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO pedidos() VALUES ()',)
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

#-------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)