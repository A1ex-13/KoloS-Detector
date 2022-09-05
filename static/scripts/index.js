var fileInput = document.querySelector('input[type=file]');
var dropImageZone = document.querySelector('.dropImageZone');
var dropText = document.querySelector('.dropText');
var imageLoader = document.getElementById('filePhoto');
var dropImageZoneImg = document.getElementById('dropImageZoneImg');
var loaderHide = document.querySelector(".hidden");
var alertHide = document.querySelector(".alert");

fileInput.addEventListener('dragenter', function() {
	dropImageZone.classList.add('dragover');
    dropText.classList.add('dragover');
}, false);

fileInput.addEventListener('dragleave', function() {
	dropImageZone.classList.remove('dragover');
    dropText.classList.remove('dragover');
}, false);

window.onload = function(){
    imageLoader.addEventListener('change', handleImage, false);
    imageLoader.addEventListener('change', submitImage, false);
}

function submitImage() { 
    setTimeout(function(){
    document.getElementById('dragDropForm').submit();
},2000)
}

function handleImage(e) {
    var file = e.target.files[0]
    var url = URL.createObjectURL(file);
    dropImageZoneImg.classList.remove("hideImage");
    dropImageZoneImg.setAttribute('src',url);
}

function showDiv(){
    loaderHide.classList.remove("hidden");
    alertHide.classList.add("hidden");
}
