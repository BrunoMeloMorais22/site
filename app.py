from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'passport'
app.config['MYSQL_DB'] = 'site'

mysql = MySQL(app)

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        telefone VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        senha VARCHAR(255) NOT NULL
    )
    ''')
    mysql.connection.commit()
    cursor.close()

@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/api/usuarios', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        senha = request.form['senha']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (nome, telefone, email, senha) VALUES (%s, %s, %s, %s)", (nome, telefone, email, senha))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('sucesso'))

@app.route('/sucesso', methods=['GET'])
def sucesso():
    return render_template('sucesso.html', message="Usuário cadastrado com sucesso!")


if __name__ == '__main__':
    app.run(debug=True)
