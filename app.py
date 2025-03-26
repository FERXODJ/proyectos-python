from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import session, flash

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

# Crando base de datos para los tickets

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True)
    analista = db.Column(db.String(50))
    status = db.Column(db.String(20))
    cliente = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

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

# Ruta para el login (nueva)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    user = Usuario.query.filter_by(usuario=usuario).first()

    if not user:
        return jsonify({'success': False, 'message': 'Usuario no existe'})
    
    if not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Contraseña incorrecta'})
    
    # Guardar usuario en sesión
    session['usuario_actual'] = user.usuario
    session['nombre_completo'] = f"{user.nombre} {user.apellido}"

    return jsonify({'success': True, 'redirect': url_for('nosotros')})

# Modifica la ruta de nosotros
@app.route('/nosotros')
def nosotros():
    if 'usuario_actual' not in session:
        return redirect(url_for('raiz'))
        
    return render_template('nosotros.html', 
                         usuario=session['nombre_completo'])

# Nueva ruta para cerrar sesión

@app.route('/logout')
def logout():
    session.pop('usuario_actual', None)
    session.pop('nombre_completo', None)
    return redirect(url_for('raiz'))

# Nueva ruta para agregar tickets

@app.route('/agregar-ticket', methods=['GET', 'POST'])
def agregar_ticket():
    if 'usuario_actual' not in session:
        return redirect(url_for('raiz'))
        
    nombre_usuario = session.get('nombre_completo', 'Invitado')
    
    if request.method == 'POST':
        try:
            nuevo_ticket = Ticket(
                numero=request.form['numero'],
                analista=request.form['analista'],
                status=request.form['status'],
                cliente=request.form['cliente'],
                usuario_id=Usuario.query.filter_by(usuario=session['usuario_actual']).first().id
            )
            db.session.add(nuevo_ticket)
            db.session.commit()
            flash('Ticket registrado exitosamente!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar el ticket: {str(e)}', 'error')
        return redirect(url_for('lista_tickets'))
        
    return render_template('agregar_ticket.html', usuario=nombre_usuario)

# Nueva ruta para listar tickets

@app.route('/lista-tickets')
def lista_tickets():
    if 'usuario_actual' not in session:
        return redirect(url_for('raiz'))
    # Obtener el nombre del usuario y los tickets
    nombre_usuario = session.get('nombre_completo', 'Invitado')
    tickets = Ticket.query.all()
    return render_template('lista_tickets.html', usuario=nombre_usuario, tickets=tickets)

# Ruta para editar tickets
@app.route('/editar-ticket/<int:id>', methods=['GET', 'POST'])
def editar_ticket(id):
    if 'usuario_actual' not in session:
        return redirect(url_for('raiz'))
    
    ticket = Ticket.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            ticket.numero = request.form['numero']
            ticket.analista = request.form['analista']
            ticket.status = request.form['status']
            ticket.cliente = request.form['cliente']
            db.session.commit()
            flash('Ticket actualizado correctamente', 'success')
            return redirect(url_for('lista_tickets'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    return render_template('editar_ticket.html', 
                        usuario=session['nombre_completo'],
                        ticket=ticket)

# Ruta para eliminar tickets
@app.route('/eliminar-ticket/<int:id>', methods=['POST'])
def eliminar_ticket(id):
    if 'usuario_actual' not in session:
        return redirect(url_for('raiz'))
    
    ticket = Ticket.query.get_or_404(id)
    try:
        db.session.delete(ticket)
        db.session.commit()
        flash('Ticket eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'error')
    
    return redirect(url_for('lista_tickets'))