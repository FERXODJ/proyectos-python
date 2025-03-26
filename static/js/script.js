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
        if (!data.success) {
            const errorContainer = document.getElementById('errorContainer');
            errorContainer.textContent = data.message;
            errorContainer.style.display = 'block';
        } else {
            // Redirección o acción exitosa
            window.location.href = '/';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});