let showActive=false
function showInformation() {
    const name = document.getElementById('name')
    const image = document.getElementById('div-image');
    const arrow = document.getElementById('arrow-info');
    const div_info = document.getElementById('div-info');
    const box_info = document.getElementById('box-info');
    if (showActive){
        name.style.visibility = "visible";
        image.style.transform = "translateX(0px)";
        div_info.style.transform = "translateX(-125px)";
        box_info.style.transition = "width 0.5s ease";
        box_info.style.width = "150px";
        box_info.style.visibility = "hidden";
        arrow.style.transition = "all 0.5s ease";
        arrow.style.transform = "rotateY(0deg)";
    }else{
        name.style.visibility = "hidden";
        image.style.transform = "translateX(-250px)";
        div_info.style.transform = "translateX(-375px)";
        box_info.style.transition = "width 1.5s ease";
        box_info.style.width="500px";
        box_info.style.visibility= "visible";
        arrow.style.transition = "all 1.5s ease";
        arrow.style.transform = "rotateY(180deg)";
    }
    showActive=!showActive
}

