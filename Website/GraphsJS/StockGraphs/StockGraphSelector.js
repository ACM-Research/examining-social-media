currentYear = 2020;

button2018 = document.getElementById("StockButton2018");
button2019 = document.getElementById("StockButton2019");
button2020 = document.getElementById("StockButton2020");

graph2018 = document.getElementById("58823d0a-23af-488c-b60b-17d5c089cdf6");
graph2019 = document.getElementById("adbcaf94-c724-4c20-9f0d-a83fae7ce7b4");
graph2020 = document.getElementById("bef75c4a-2b2d-44c9-bd9c-0575533f8560");


UpdateGraph = () => {
    switch(currentYear){
        case 2018:
            graph2018.style.display = "block";
            graph2019.style.display = "none";
            graph2020.style.display = "none";
            break;
        case 2019:
            graph2018.style.display = "none";
            graph2019.style.display = "block";
            graph2020.style.display = "none";
            break;
        case 2020:
            graph2018.style.display = "none";
            graph2019.style.display = "none";
            graph2020.style.display = "block";
            break;
    }
    
}
UpdateGraph();

button2018.onclick = () => {
    currentYear = 2018;
    UpdateGraph();
};

button2019.onclick = () => {
    currentYear = 2019;
    UpdateGraph();
};

button2020.onclick = () => {
    currentYear = 2020;
    UpdateGraph();
};
