document.getElementById("semd_comment").addEventListener("submit", async(event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const label_icono = document.getElementById("label_icono_comment");
    label_icono.innerHTML == "Comentario publico" ? is_public = true : is_public = false
    formData.append('is_public', is_public);
    const data = Object.fromEntries(formData.entries());
    const urlParams = new URLSearchParams(window.location.search);
    const slug = urlParams.get('slug');
    const response = await fetch('/post?slug='+slug, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    if (response.status === 400) {
        alert(result.message);
    } else {
        window.location.href = "/post?slug="+slug;
    }
});

document.getElementById("is_public").addEventListener("click",()=>{
    const icono = document.getElementById("icon_type_comment");
    const label_icono = document.getElementById("label_icono_comment");
    icono.classList.contains('bi-globe-americas') ? icono.classList.replace('bi-globe-americas', 'bi-person-fill') : icono.classList.replace('bi-person-fill', 'bi-globe-americas');
    label_icono.innerHTML=="Comentario publico" ? label_icono.innerHTML="Comentario privado" : label_icono.innerHTML="Comentario publico"
});