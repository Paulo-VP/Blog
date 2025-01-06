function seePassword(element) {
    element.type = element.type === 'password' ? 'text' : 'password';
    const icono = document.getElementById(element.id + "_icon");
    icono.classList.contains('bi-eye-slash') ? icono.classList.replace('bi-eye-slash', 'bi-eye') : icono.classList.replace('bi-eye', 'bi-eye-slash');
}

