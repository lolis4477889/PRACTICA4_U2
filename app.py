from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'ACL2005'  # Ajustar si tienes contraseña
DB_NAME = 'bd_cafeteria'

def get_db_connection():
    return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/agregar', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    calle = request.form['calle']
    colonia = request.form['colonia']
    referencia = request.form['referencia']
    telefono = request.form['telefono']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (Nombre_Cliente, Calle, Colonia, Referencia_Casa, Telefono) VALUES (%s, %s, %s, %s, %s)",
                   (nombre, calle, colonia, referencia, telefono))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/eliminar/<int:id_cliente>')
def eliminar_cliente(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE ID_CLIENTE = %s", (id_cliente,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/actualizar', methods=['POST'])
def actualizar_cliente():
    id_cliente = request.form['id_cliente']
    nombre = request.form['nombre']
    calle = request.form['calle']
    colonia = request.form['colonia']
    referencia = request.form['referencia']
    telefono = request.form['telefono']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET Nombre_Cliente=%s, Calle=%s, Colonia=%s, Referencia_Casa=%s, Telefono=%s WHERE ID_CLIENTE=%s",
                   (nombre, calle, colonia, referencia, telefono, id_cliente))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    
