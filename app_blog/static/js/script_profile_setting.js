function showImage() {
    document.getElementById('imageSection').style.display="block";
    document.getElementById('nameSection').style.display="none";
    document.getElementById('mailSection').style.display="none";
    document.getElementById('passwordSection').style.display = "none";
    document.getElementById('deleteSection').style.display = "none";
}

function showUserData() {
    document.getElementById('nameSection').style.display="block";
    document.getElementById('imageSection').style.display="none";
    document.getElementById('mailSection').style.display="none";
    document.getElementById('passwordSection').style.display="none";
    document.getElementById('deleteSection').style.display = "none";

}

function showMail() {
    document.getElementById('mailSection').style.display="block";
    document.getElementById('imageSection').style.display="none";
    document.getElementById('nameSection').style.display="none";
    document.getElementById('passwordSection').style.display="none";
    document.getElementById('deleteSection').style.display = "none";

}

function showPassword() {
    document.getElementById('passwordSection').style.display="block";
    document.getElementById('imageSection').style.display="none";
    document.getElementById('nameSection').style.display="none";
    document.getElementById('mailSection').style.display="none";
    document.getElementById('deleteSection').style.display = "none";
}

function showDelete() {
    document.getElementById('deleteSection').style.display = "block";
    document.getElementById('imageSection').style.display = "none";
    document.getElementById('nameSection').style.display = "none";
    document.getElementById('mailSection').style.display = "none";
    document.getElementById('passwordSection').style.display = "none";
}

document.getElementById('imageSection').addEventListener('submit', async (event) => {
    event.preventDefault();
    const image = document.getElementById("profile_image").src
    const form = event.target;
    const formData = new FormData(form);
    formData.append('action', 'setImage');
    formData.append('image', image);
    const data = Object.fromEntries(formData.entries());
    const response = await fetch('/profile/setting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    if (response.status === 400) {
        alert(result.message);
    } else {
    }
});

document.getElementById('nameSection').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    formData.append('action', 'setName');
    const data = Object.fromEntries(formData.entries());
    const response = await fetch('/profile/setting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    if (response.status === 400) {
        alert(result.message);
    } else {
    }
});

document.getElementById('passwordSection').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    formData.append('action', 'setPassword');
    const data = Object.fromEntries(formData.entries());
    const response = await fetch('/profile/setting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    if (response.status === 400) {
        alert(result.message);
    } else {
    }
});