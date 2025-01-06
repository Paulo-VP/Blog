function showCreateAccount() {
    document.getElementById('loginSection').style.display="none";
    document.getElementById('createAccountSection').style.display="block";
}

function showForgotPassword() {
    document.getElementById('loginSection').style.display="none";
    document.getElementById('forgotPasswordSection').style.display="block";
}

function showLogin() {
    document.getElementById('createAccountSection').style.display="none";
    document.getElementById('forgotPasswordSection').style.display="none";
    document.getElementById('loginSection').style.display="block";
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
    console.log(result)
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
    console.log(result)
});