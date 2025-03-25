const fondo = document.querySelector('.fondo');
const btnSingIn = document.getElementById('btn_singin');
const btnSingUp = document.getElementById('btn_singup');

btnSingIn.addEventListener('click', () => {

    fondo.classList.remove('toggle');

});

btnSingUp.addEventListener('click', () => {
    fondo.classList.add('toggle');
});