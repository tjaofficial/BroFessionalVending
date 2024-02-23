
autoAddSold = (elem) => {
    const selectionID = String(elem.id.replace('id_stock_', ''));
    const soldInput = document.getElementById('id_sold_'+ selectionID);
    const prevQty = parseInt(elem.parentNode.parentNode.children[2].children[0].value);
    const currentQty = parseInt(elem.value)
    const amountSold = prevQty - currentQty
    console.log(amountSold);
    soldInput.value = amountSold;
}

requireDate = (elem) => {
    const selectionID = String(elem.id.replace('id_added_', ''));
    const soldInput = parseInt(elem.value);
    const newDate = document.getElementById('id_new_dates_'+ selectionID);
    const prevInven = document.getElementById('prevInventory').dataset.prev;

    if(soldInput > 0){
        newDate.required = true;
        newDate.disabled = false;
    } else {
        newDate.required = false;
        newDate.disabled = true;
    }

}

