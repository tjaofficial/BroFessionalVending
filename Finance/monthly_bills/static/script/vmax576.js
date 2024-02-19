function autoFill(number){
    const lane = document.getElementById('id_stock_' + String(number));
    const oldLane = JSON.parse(document.getElementById('lane_' + String(number)).dataset.lane);
    const sold = parseInt(oldLane.total) - parseInt(lane.value);
    document.getElementById('id_sold_'+String(number)).value = sold;
}



