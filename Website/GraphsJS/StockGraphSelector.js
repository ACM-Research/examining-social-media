var currentYear = 2018;

let button2018Stock = document.getElementById("StockButton2018");
let button2019Stock = document.getElementById("StockButton2019");
let button2020Stock = document.getElementById("StockButton2020");

let graph2018Stock = document.getElementById("44feaffe-72c4-4214-97ce-8e039f43f006");
let graph2019Stock = document.getElementById("92dc78c8-c438-4d2c-8277-8a4e9e826a8d");
let graph2020Stock = document.getElementById("d1e1cad0-86c2-47f5-9752-3074426c7994");

var things= "oiajsd";

function UpdateGraphStock(){
    console.log("switching")
    switch(currentYear){
        case 2018:
            graph2018Stock.style.display = "block";
            graph2019Stock.style.display = "none";
            graph2020Stock.style.display = "none";
            break;
        case 2019:
            graph2018Stock.style.display = "none";
            graph2019Stock.style.display = "block";
            graph2020Stock.style.display = "none";
            break;
        case 2020:
            graph2018Stock.style.display = "none";
            graph2019Stock.style.display = "none";
            graph2020Stock.style.display = "block";
            break;
    }
    return;
    
}
UpdateGraphStock();

button2018Stock.onclick = () => {
    currentYear = 2018;
    UpdateGraphStock();
};

button2019Stock.onclick = () => {
    currentYear = 2019;
    UpdateGraphStock();
};

button2020Stock.onclick = () => {
    currentYear = 2020;
    UpdateGraphStock();
};
