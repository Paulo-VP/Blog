const passwordInput = document.getElementById('password');
const password2Input = document.getElementById('password2');

passwordInput.addEventListener('input', () => {
    const password = passwordInput.value;
    const password2 = password2Input.value;
    document.getElementById('length').style.color = password.length >= 8 ? 'green' : 'red';
    document.getElementById('capital').style.color = /[A-Z]/.test(password) ? 'green' : 'red';
    document.getElementById('lower').style.color = /[a-z]/.test(password) ? 'green' : 'red';
    document.getElementById('number').style.color = /[0-9]/.test(password) ? 'green' : 'red';
    document.getElementById('symbol').style.color = /[!@#$%^&*()_,.?":{}|<>]/.test(password) ? 'green' : 'red';
    document.getElementById('equals').style.color = password === password2 ? 'green' : 'red';

});

password2Input.addEventListener('input', () => {
    const password = passwordInput.value;
    const password2 = password2Input.value;
    document.getElementById('equals').style.color = password === password2 ? 'green' : 'red';
});

function asd(password) {
    return (
        password.length >= 8 &&
        /[A-Z]/.test(password) &&
        /[a-z]/.test(password) &&
        /[0-9]/.test(password) &&
        /[!@#$%^&*(),.?":{}|<>]/.test(password)
    );
}