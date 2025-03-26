from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para usar flash

@app.route('/', methods=['GET', 'POST'])
def raiz():
    if request.method == 'POST':
        # Verificar si es JSON (petición AJAX)
        if request.is_json:
            data = request.get_json()
            password = data.get('password')
            password2 = data.get('password2')
            
            if password != password2:
                return jsonify({'success': False, 'message': 'Las contraseñas no coinciden'})
            
            # Aquí iría el resto de la lógica de registro...
            return jsonify({'success': True})
            
        # Mantener la lógica original para compatibilidad
        elif 'password' in request.form and 'password2' in request.form:
            password = request.form['password']
            password2 = request.form['password2']
            
            if password != password2:
                flash('Las contraseñas no coinciden', 'error')
                return redirect(url_for('raiz'))
    
    return render_template('index.html')
#ruta paa nosotros
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

#Bloque de Prueba

if __name__ == '__main__':
    app.run(debug=True)

def vercel_handler(request):
    with app.app_context():
        response = app.full_dispatch_request()()
        return response