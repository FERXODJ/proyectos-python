//Manejo de la animación de los formularios de inicio de sesión y registro

const fondo = document.querySelector('.fondo');
const btnSingIn = document.getElementById('btn_singin');
const btnSingUp = document.getElementById('btn_singup');

btnSingIn.addEventListener('click', () => {

    fondo.classList.remove('toggle');

});

btnSingUp.addEventListener('click', () => {
    fondo.classList.add('toggle');
});

// Si hay mensajes de error en registro, muestra ese formulario
if(document.querySelector('.registro .alert')) {
    document.querySelector('.registro').style.display = 'block';
    document.querySelector('.inicio-sesion').style.display = 'none';
}

//Manera de registro

document.getElementById('registroForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        email: document.getElementById('email').value,
        usuario: document.getElementById('usuario_registro').value,
        password: document.getElementById('password_registro').value,
        password2: document.getElementById('password2').value,
        cargo: document.getElementById('cargo').value
    };

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        const errorContainer = document.getElementById('errorContainer');
        if (!data.success) {
            errorContainer.textContent = data.message;
            errorContainer.style.display = 'block';
        } else {
            errorContainer.style.color = 'green';
            errorContainer.textContent = data.message;
            errorContainer.style.display = 'block';
            
            // Redirección después de 3 segundos
            setTimeout(() => {
                window.location.href = '/';
            }, 3000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Manejar login
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const loginData = {
        usuario: document.getElementById('usuario').value,
        password: document.getElementById('password').value
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
        const errorContainer = document.getElementById('loginError');
        if (!data.success) {
            errorContainer.textContent = data.message;
            errorContainer.style.display = 'block';
        } else {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Resaltar solo el enlace activo
function actualizarEnlaceActivo() {
    const enlaces = document.querySelectorAll('.nav-link');
    const rutaActual = window.location.pathname;
    
    enlaces.forEach(enlace => {
        enlace.classList.remove('active');
        if (enlace.getAttribute('href') === rutaActual) {
            enlace.classList.add('active');
        }
    });
}

// Ejecutar al cargar y después de navegar
document.addEventListener('DOMContentLoaded', actualizarEnlaceActivo);
window.addEventListener('popstate', actualizarEnlaceActivo);