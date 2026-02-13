const file_inp=document.getElementById("resume-input");
const subtitle=document.querySelector(".upload-subtitle")
const uploadBox = document.querySelector(".upload-box");

file_inp.addEventListener("change",function(){
    if(file_inp.files.length > 0){
        subtitle.textContent= file_inp.files[0].name + " selected";
        uploadBox.classList.add("active");
        uploadBox.classList.add("loading");
        file_inp.form.submit();
    }
});
uploadBox.addEventListener("dragover",function(e){
    e.preventDefault();
    uploadBox.classList.add("dragover");
});
uploadBox.addEventListener("dragleave",function(e){
    e.preventDefault();
    uploadBox.classList.remove("dragover");
});
uploadBox.addEventListener("drop",function(e){
    e.preventDefault();
    uploadBox.classList.remove("dragover");
    if(e.dataTransfer.files.length >0){
        file_inp.files=e.dataTransfer.files;
        subtitle.textContent=file_inp.files[0].name + " selected";
        uploadBox.classList.add("active");
        uploadBox.classList.add("loading");
        file_inp.form.submit();
    }
});
