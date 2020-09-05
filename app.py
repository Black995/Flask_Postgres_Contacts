from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)

# Database configuration
# Connect to your postgres DB
conn = psycopg2.connect("dbname=flask_fazt_db user=postgres password=12345")
# Open a cursor to perform database operations
#cur = conn.cursor()

# Settings
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall()
    return render_template('index.html', contactos=data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = conn.cursor()
        cur.execute('INSERT INTO contactos (nombre, telefono, email) VALUES (%s, %s, %s)',
                    (nombre, telefono, email))
        cur.connection.commit()

        flash('Contacto agregado satisfactoriamente')
    return redirect(url_for('index'))


@app.route('/edit/<string:id>')
def edit_contact(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('EditContact.html', contact=data[0])


@app.route('/update/<string:id>', methods=['POST'])
def updateContact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = conn.cursor()
        cur.execute("""
            UPDATE contactos
            SET nombre = %s,
                telefono = %s,
                email = %s
            WHERE id = %s
        """, (nombre, telefono, email, id))
        cur.connection.commit()
        flash('Contacto actualizado satisfactoriamente')
    return redirect(url_for('index'))


@app.route('/delete/<string:id>',)
def delete_contact(id):
    cur = conn.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    cur.connection.commit()
    flash('Contacto removido satisfactoriamente')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
