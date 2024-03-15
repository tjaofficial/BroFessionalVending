
// for(i=1; i<=5; i++){
//     document.getElementById('id_stock_A' + String(i)).addEventListener('change', doMath)
// }

// for(i=1; i<=6; i++){
//     document.getElementById('id_stock_B' + String(i)).addEventListener('change', doMath)
// }

// for(i=1; i<=10; i++){
//     document.getElementById('id_stock_C' + String(i)).addEventListener('change', doMath)
// }

// for(i=1; i<=8; i++){
//     document.getElementById('id_stock_D' + String(i)).addEventListener('change', doMath)
// }

// function doMath(){
//     for(i=1; i<=5; i++){
//         const prevA = document.getElementById('prevA' + String(i)).value;
//         const stockA = document.getElementById('id_stock_A' + String(i)).value;
//         const addedA = document.getElementById('id_added_A' + String(i)).value;
//         if (prevA - stockA == prevA){
//             document.getElementById('id_sold_A' + String(i)).value = 0;
//         } else {
//             document.getElementById('id_sold_A' + String(i)).value = prevA - stockA;
//         }
        
//         //document.getElementById('').value = stockA + addedA;
//     }
//     for(i=1; i<=6; i++){
//         const prevB = document.getElementById('prevB' + String(i)).value;
//         const stockB = document.getElementById('id_stock_B' + String(i)).value;
//         const addedB = document.getElementById('id_added_B' + String(i)).value;
//         if (prevB - stockB == prevB){
//             document.getElementById('id_sold_B' + String(i)).value = 0;
//         } else {
//             document.getElementById('id_sold_B' + String(i)).value = prevB - stockB;
//         }
        
//         //document.getElementById('').value = stockB + addedB;
//     }
//     for(i=1; i<=10; i++){
//         const prevC = document.getElementById('prevC' + String(i)).value;
//         const stockC = document.getElementById('id_stock_C' + String(i)).value;
//         const addedC = document.getElementById('id_added_C' + String(i)).value;
//         if (prevC - stockC == prevC){
//             document.getElementById('id_sold_C' + String(i)).value = 0;
//         } else {
//             document.getElementById('id_sold_C' + String(i)).value = prevC - stockC;
//         }
        
//         //document.getElementById('').value = stockC + addedC;
//     }
//     for(i=1; i<=8; i++){
//         const prevD = document.getElementById('prevD' + String(i)).value;
//         const stockD = document.getElementById('id_stock_D' + String(i)).value;
//         const addedD = document.getElementById('id_added_D' + String(i)).value;
//         if (prevD - stockD == prevD){
//             document.getElementById('id_sold_D' + String(i)).value = 0;
//         } else {
//             document.getElementById('id_sold_D' + String(i)).value = prevD - stockD;
//         }
        
//         //document.getElementById('').value = stockD + addedD;
//     }
// }
// doMath();