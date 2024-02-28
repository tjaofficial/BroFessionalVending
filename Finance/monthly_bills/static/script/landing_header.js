function toggleDropDown(){
    const dropDownMenu = document.getElementById('dropDownMenu').children[0];
    console.log(dropDownMenu.style.display)
    if (dropDownMenu.style.display == 'none') {
        dropDownMenu.style.display = 'block';
    } else if (dropDownMenu.style.display == 'block') {
        dropDownMenu.style.display = 'none';
    }
}