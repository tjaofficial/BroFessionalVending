function toggleBuildsInput(){
    const displayInput = document.getElementById('buildInput');
    if (displayInput.style.display == "none"){
        displayInput.style.display = "table-row";
    } else {
        displayInput.style.display = "none";
    }
}