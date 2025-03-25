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