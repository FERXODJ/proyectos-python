from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de Usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    usuario = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    cargo = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear tablas
with app.app_context():
    db.create_all()

# Rutas
@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        usuario = request.form['usuario']
        password = request.form['password']
        password2 = request.form['password2']
        cargo = request.form['cargo']

        if password != password2:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('index'))

        if User.query.filter_by(usuario=usuario).first():
            flash('El usuario ya existe', 'error')
            return redirect(url_for('index'))

        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return redirect(url_for('index'))

        nuevo_usuario = User(
            nombre=nombre,
            apellido=apellido,
            email=email,
            usuario=usuario,
            password=generate_password_hash(password),
            cargo=cargo
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso! Por favor inicia sesión', 'success')
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']
    user = User.query.filter_by(usuario=usuario).first()

    if not user or not check_password_hash(user.password, password):
        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('index'))
    
    login_user(user)
    return redirect(url_for('home'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)