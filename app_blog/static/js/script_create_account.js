document.getElementById('createForm').addEventListener('submit', async (event) => {
    event.preventDefault(); 
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');  
    const response = await fetch('/create?token=' + token, {
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
