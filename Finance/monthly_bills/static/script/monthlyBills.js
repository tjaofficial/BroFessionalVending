document.getElementById('id_bill').addEventListener('change', grabData);

function grabData(){
    const data = JSON.parse(document.getElementById('billData').getAttribute('data-bills'));
    console.log(data);
}