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

document.getElementById('loginSection').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    formData.append('action', 'login');
    const data = Object.fromEntries(formData.entries());
    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    console.log(result);
    if (response.status === 400) {
        alert(result.message);
    } else {
        window.location.href = "/";
    }
});

document.getElementById('createAccountSection').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    formData.append('action', 'create');
    const data = Object.fromEntries(formData.entries());
    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    console.log(result);
});

document.getElementById('forgotPasswordSection').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    formData.append('action', 'recovery');
    const data = Object.fromEntries(formData.entries());
    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    console.log(result);
});