function addShit(){
    const p1Button = document.getElementById('addButtonP1');
    const p2Button = document.getElementById('addButtonP2');
    const p3Button = document.getElementById('addButtonP3');
    const p4Button = document.getElementById('addButtonP4');
    const p5Button = document.getElementById('addButtonP5');
    const p6Button = document.getElementById('addButtonP6');
    const p7Button = document.getElementById('addButtonP7');
    const p8Button = document.getElementById('addButtonP8');
    p1Button.onclick = function(){myFunction('1')};
    p2Button.onclick = function(){myFunction('2')};
    p3Button.onclick = function(){myFunction('3')};
    p4Button.onclick = function(){myFunction('4')};
    p5Button.onclick = function(){myFunction('5')};
    p6Button.onclick = function(){myFunction('6')};
    p7Button.onclick = function(){myFunction('7')};
    p8Button.onclick = function(){myFunction('8')};
    
    function myFunction(num) {
        const prod = document.getElementById('addP' + num);
        console.log('addP' + num)
        if (prod.style.visibility == 'hidden' || !prod.style.visibility){
            prod.style.visibility = 'visible';
        } else {
            prod.style.visibility = 'hidden';
        }
    }
}
addShit();
function soldShit(){
    const p1Button = document.getElementById('soldButtonP1');
    const p2Button = document.getElementById('soldButtonP2');
    const p3Button = document.getElementById('soldButtonP3');
    const p4Button = document.getElementById('soldButtonP4');
    const p5Button = document.getElementById('soldButtonP5');
    const p6Button = document.getElementById('soldButtonP6');
    const p7Button = document.getElementById('soldButtonP7');
    const p8Button = document.getElementById('soldButtonP8');
    p1Button.onclick = function(){myFunction('1')};
    p2Button.onclick = function(){myFunction('2')};
    p3Button.onclick = function(){myFunction('3')};
    p4Button.onclick = function(){myFunction('4')};
    p5Button.onclick = function(){myFunction('5')};
    p6Button.onclick = function(){myFunction('6')};
    p7Button.onclick = function(){myFunction('7')};
    p8Button.onclick = function(){myFunction('8')};
    
    function myFunction(num) {
        const prod = document.getElementById('soldP' + num);
        console.log('soldP' + num)
        if (prod.style.visibility == 'hidden' || !prod.style.visibility){
            prod.style.visibility = 'visible';
        } else {
            prod.style.visibility = 'hidden';
        }
    }
}
soldShit();