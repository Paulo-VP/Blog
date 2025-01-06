let cropper;

document.getElementById('input_file').onchange = function (evt) {
    const button = document.getElementById('crop_button');
    const files = evt.target.files[0];
    button.style.display="block";
    if (files) {
        const fr = new FileReader();
        fr.onload = function (e) {
            document.getElementById("image").src = e.target.result;
            cargarCropper();
        }
        fr.readAsDataURL(files);
    }

}

function getRoundedCanvas(sourceCanvas) {
    let canvas = document.createElement('canvas');
    let context = canvas.getContext('2d');
    let width = sourceCanvas.width;
    let height = sourceCanvas.height;
    canvas.width = width;
    canvas.height = height;
    context.imageSmoothingEnabled = true;
    context.drawImage(sourceCanvas, 0, 0, width, height);
    context.globalCompositeOperation = 'destination-in';
    context.beginPath();
    context.arc(width / 2, height / 2, Math.min(width, height) / 2, 0, 2 * Math.PI, true);
    context.fill();
    return canvas;
}

function cargarCropper() {
    let image = document.getElementById('image');
    let button = document.getElementById('crop_button');
    let result = document.getElementById('profile_image');
    image.style.width = `${window.innerWidth * 0.8}px`; 
    let croppable = false;
    let minCroppedWidth = 160;
    let minCroppedHeight = 160;
    let maxCroppedWidth = 460;
    let maxCroppedHeight = 460;
    if (cropper) {
        cropper.destroy();
    }
    cropper = new Cropper(image, {
        aspectRatio: 1,
        viewMode: 3,
        zoomable: false,
        data: {
            width: (minCroppedWidth + maxCroppedWidth) / 2,
            height: (minCroppedHeight + maxCroppedHeight) / 2,
        },  
        crop: function (event) {
            let width = Math.round(event.detail.width);
            let height = Math.round(event.detail.height);
            if (width < minCroppedWidth || height < minCroppedHeight || width > maxCroppedWidth || height > maxCroppedHeight) {
                cropper.setData({
                    width: Math.max(minCroppedWidth, Math.min(maxCroppedWidth, width)),
                    height: Math.max(minCroppedHeight, Math.min(maxCroppedHeight, height)),
                });
            }
        },
        ready: function () {
            croppable = true;
        },
    });
    button.onclick = function () {
        let croppedCanvas;
        let roundedCanvas;
        if (!croppable) {
            return;
        }
        croppedCanvas = cropper.getCroppedCanvas();
        roundedCanvas = getRoundedCanvas(croppedCanvas);
        result.src = roundedCanvas.toDataURL();
    };
};