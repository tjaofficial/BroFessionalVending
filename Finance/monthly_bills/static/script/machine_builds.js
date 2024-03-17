displaySnackLanes = (elem) => {
    const numberOfSnackLanes = elem.value;
    let htmlCode = ""
    const laneSnackGrab = document.getElementById('laneSnackGrab')
    for(let x=1; x<=parseInt(numberOfSnackLanes); x++){
        let parseLane = laneSnackGrab.innerHTML.replace(`name="size"`, `name="size_S${x}"`).replace(`name="slots"`, `name="slots_S${x}"`).replace(`name="selectID"`, `name="selectID_S${x}"`).replace(`name="itemID"`, `name="itemID_S${x}"`).replace(`name="cost"`, `name="cost_S${x}"`);
        htmlCode += parseLane;
    }
    const snackCont = document.getElementById('snackCont');
    snackCont.innerHTML = htmlCode;
}

displayDrinkLanes = (elem) => {
    const numberOfDrinkLanes = elem.value;
    let htmlCode = ""
    const laneDrinkGrab = document.getElementById('laneDrinkGrab')
    for(let x=1; x<=parseInt(numberOfDrinkLanes); x++){
        let parseLane = laneDrinkGrab.innerHTML.replace(`name="size"`, `name="size_D${x}"`).replace(`name="slots"`, `name="slots_D${x}"`).replace(`name="selectID"`, `name="selectID_D${x}"`).replace(`name="itemID"`, `name="itemID_D${x}"`).replace(`name="cost"`, `name="cost_D${x}"`);
        htmlCode += parseLane;
    }
    const drinkCont = document.getElementById('drinkCont');
    drinkCont.innerHTML = htmlCode;
}

const snackLanes = document.getElementById('snack_lane_qty').value;
const drinkLanes = document.getElementById('drink_lane_qty').value;

if (snackLanes) {
    let htmlCode = ""
    const laneSnackGrab = document.getElementById('laneSnackGrab')
    for(let x=1; x<=parseInt(snackLanes); x++){
        let parseLane = laneSnackGrab.innerHTML.replace(`name="size"`, `name="size_S${x}"`).replace(`name="slots"`, `name="slots_S${x}"`).replace(`name="selectID"`, `name="selectID_S${x}"`).replace(`name="itemID"`, `name="itemID_S${x}"`).replace(`name="cost"`, `name="cost_S${x}"`);
        htmlCode += parseLane;
    }
    const snackCont = document.getElementById('snackCont');
    snackCont.innerHTML = htmlCode;
}

if (drinkLanes) {
    let htmlCode = ""
    const laneDrinkGrab = document.getElementById('laneDrinkGrab')
    for(let x=1; x<=parseInt(drinkLanes); x++){
        let parseLane = laneDrinkGrab.innerHTML.replace(`name="size"`, `name="size_D${x}"`).replace(`name="slots"`, `name="slots_D${x}"`).replace(`name="selectID"`, `name="selectID_D${x}"`).replace(`name="itemID"`, `name="itemID_D${x}"`).replace(`name="cost"`, `name="cost_D${x}"`);
        htmlCode += parseLane;
    }
    const drinkCont = document.getElementById('drinkCont');
    drinkCont.innerHTML = htmlCode;
}