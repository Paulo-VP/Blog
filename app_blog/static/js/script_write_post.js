const background_color = document.getElementById('background-color');
const font_color = document.getElementById('font-color');
const card_title = document.getElementById('card-title');
const dynamic_input = document.getElementById('dynamic-input');
const name_card = document.getElementById('name-card');
const date_card = document.getElementById('date-card');


background_color.addEventListener('input', function () {;
    card_title.style.background = event.target.value;
});

font_color.addEventListener('input', function () {
    const color = event.target.value;
    dynamic_input.style.color = color;
    name_card.style.color = color;
    date_card.style.color = color;
});

dynamic_input.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});


const toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    //['table'],
    ['blockquote', 'code-block'],
    ['link', 'image', 'video'],
    [{ 'list': 'ordered' }, { 'list': 'bullet' }, { 'list': 'check' }],
    [{ 'script': 'sub' }, { 'script': 'super' }, 'formula'],
    [{ 'indent': '-1' }, { 'indent': '+1' }],
    [{ 'size': ['small', false, 'large', 'huge'] }],  
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
    [{ 'color': [] }, { 'background': [] }],          
    [{ 'font': [] }],
    [{ 'align': [] }],
    ['clean']                                         
];

var quill = new Quill('#editor', {
    theme: 'snow',
    modules: {
        toolbar: toolbarOptions
    }
});

document.getElementById('save-post').addEventListener('click', async() => {
    const title = dynamic_input.value;
    const text_color = dynamic_input.style.color || "rgb(0, 0, 0)";
    const card_color = card_title.style.background || "rgb(255, 255, 255)";
    const editorContent = quill.root.innerHTML;
    if (editorContent){
        const response = await fetch('/post/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, text_color, card_color, editor_content: editorContent })
        })
        const result = await response.json();
        if (response.status === 400) {
            alert(result.message); 
        } else {
            alert(result.message); 
        }
    }
});

