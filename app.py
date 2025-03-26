from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)
app.secret_key = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)

# Modelo de la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    usuario = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    cargo = db.Column(db.String(50))

# Crear tablas al iniciar
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def raiz():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            
            # Verificar si el usuario o email ya existen
            if Usuario.query.filter_by(usuario=data['usuario']).first():
                return jsonify({'success': False, 'message': 'El usuario ya existe'})
                
            if Usuario.query.filter_by(email=data['email']).first():
                return jsonify({'success': False, 'message': 'El email ya está registrado'})

            if data['password'] != data['password2']:
                return jsonify({'success': False, 'message': 'Las contraseñas no coinciden'})

            # Crear nuevo usuario
            nuevo_usuario = Usuario(
                nombre=data['nombre'],
                apellido=data['apellido'],
                email=data['email'],
                usuario=data['usuario'],
                password=generate_password_hash(data['password']),
                cargo=data['cargo']
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Registro exitoso!'})
    
    return render_template('index.html')

# ... resto del código ...
#ruta paa nosotros
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

#Bloque de Prueba

if __name__ == '__main__':
    app.run(debug=True)

# Para compatibilidad con Vercel
def vercel_handler(request):
    with app.app_context():
        response = app.full_dispatch_request()()
        return response