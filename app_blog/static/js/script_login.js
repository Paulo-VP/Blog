function showCreateAccount() {
    document.getElementById('loginSection').classList.add('hidden');
    document.getElementById('createAccountSection').classList.remove('hidden');
}

function showForgotPassword() {
    document.getElementById('loginSection').classList.add('hidden');
    document.getElementById('forgotPasswordSection').classList.remove('hidden');
}

function showLogin() {
    document.getElementById('createAccountSection').classList.add('hidden');
    document.getElementById('forgotPasswordSection').classList.add('hidden');
    document.getElementById('loginSection').classList.remove('hidden');
}