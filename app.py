from flask import Flask, render_template , redirect, session, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from consultas import consulta, insertar

contraseña_segura= generate_password_hash("2025")
print("mi contraseña segura:" ,contraseña_segura)

# contraseña_usuario =input("contraseña: ")
# if check_password_hash(contraseña_segura, contraseña_usuario):
#     print("contraseña correcta")
# else :
#     print("contraseña incorrecta")

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        usuario = request.form['user']
        password_plana = request.form['password']

        # 1. Verificar si el usuario ya existe en la BD
        query_verificar = "SELECT * FROM usuarios WHERE user = %s"
        existe = consulta(query_verificar, (usuario,))

        if existe:
            flash('El nombre de usuario ya está registrado', 'error')
            return redirect(url_for('registro'))

        # 2. Generar el hash de la contraseña ingresada
        password_hash = generate_password_hash(password_plana)

        # 3. Insertar el nuevo usuario con la contraseña hasheada
        query_insertar = "INSERT INTO usuarios (nombre, user, clave) VALUES (%s, %s, %s)"
        exito = insertar(query_insertar, (nombre, usuario, password_hash))

        if exito:
            flash('Usuario registrado exitosamente. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al conectar con la base de datos al registrar.', 'error')

    return render_template('registro.html')

#mostrar iniciar sesion
@app.route('/')
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        usuario = request.form['user']
        password_ingresada = request.form['password']

        query = "SELECT * FROM usuarios WHERE user = %s"
        resultado = consulta(query, (usuario,))

        if resultado:
            usuario_db = resultado[0] 
            hash_almacenado = usuario_db['clave'] 

            if check_password_hash(hash_almacenado, password_ingresada):
                session['usuario_id'] = usuario_db['id']
                session['usuario_nombre'] = usuario_db['user']
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('dashboard')) 
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('El usuario no existe', 'error')

    return render_template('/login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' in session:
        return f"Bienvenido, {session['usuario_nombre']}!"
    return redirect(url_for('login'))

app.run(debug=True)