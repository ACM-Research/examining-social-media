currentYear = 2020;

button2018Sentiment = document.getElementById("SentimentButton2018");
button2019Sentiment = document.getElementById("SentimentButton2019");
button2020Sentiment = document.getElementById("SentimentButton2020");

graph2018Sentiment = document.getElementById("80f6b50d-b7f1-4b96-92e7-7721a04cea54");
graph2019Sentiment = document.getElementById("b3abc778-7516-4b35-9dfd-8efdbb5db85f");
graph2020Sentiment = document.getElementById("5b872375-003e-473f-a01d-4e607af8f78b");


UpdateGraphSentiment = () => {
    switch(currentYear){
        case 2018:
            graph2018Sentiment.style.display = "block";
            graph2019Sentiment.style.display = "none";
            graph2020Sentiment.style.display = "none";
            break;
        case 2019:
            graph2018Sentiment.style.display = "none";
            graph2019Sentiment.style.display = "block";
            graph2020Sentiment.style.display = "none";
            break;
        case 2020:
            graph2018Sentiment.style.display = "none";
            graph2019Sentiment.style.display = "none";
            graph2020Sentiment.style.display = "block";
            break;
    }
    
}
UpdateGraphSentiment();

button2018Sentiment.onclick = () => {
    currentYear = 2018;
    UpdateGraphSentiment();
};

button2019Sentiment.onclick = () => {
    currentYear = 2019;
    UpdateGraphSentiment();
};

button2020Sentiment.onclick = () => {
    currentYear = 2020;
    UpdateGraphSentiment();
};
