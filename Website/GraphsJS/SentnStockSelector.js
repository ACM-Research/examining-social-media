var currentYear = 2020;

let button2018SentStock = document.getElementById("SentStockButton2018");
let button2019SentStock = document.getElementById("SentStockButton2019");
let button2020SentStock = document.getElementById("SentStockButton2020");

let graph2018SentStock = document.getElementById("53f782f5-544e-493b-8ec7-f66e1ce41bcb");
let graph2019SentStock = document.getElementById("31dc0a1e-213a-4732-ab8e-54884ae26132");
let graph2020SentStock = document.getElementById("f9a72f18-2ee4-487a-9e15-30fcfc4cee5f");

var things= "oiajsd";

function UpdateGraphSentStock(){
    console.log("switching")
    switch(currentYear){
        case 2018:
            graph2018SentStock.style.display = "block";
            graph2019SentStock.style.display = "none";
            graph2020SentStock.style.display = "none";
            break;
        case 2019:
            graph2018SentStock.style.display = "none";
            graph2019SentStock.style.display = "block";
            graph2020SentStock.style.display = "none";
            break;
        case 2020:
            graph2018SentStock.style.display = "none";
            graph2019SentStock.style.display = "none";
            graph2020SentStock.style.display = "block";
            break;
    }
    return;
    
}
UpdateGraphSentStock();

button2018SentStock.onclick = () => {
    currentYear = 2018;
    UpdateGraphSentStock();
};

button2019SentStock.onclick = () => {
    currentYear = 2019;
    UpdateGraphSentStock();
};

button2020SentStock.onclick = () => {
    currentYear = 2020;
    UpdateGraphSentStock();
};
