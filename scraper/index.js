const puppeteer = require("puppeteer");
const { hashTweetData } = require("./util");


const PAGE_URL_START = "https://twitter.com/search?q=%23NETFLIX%20until%3A";
const PAGE_URL_MID = "%20since%3A";
const PAGE_URL_END = "&src=typed_query&f=top";

//Month starts from 0 so minus the actual month by 1
//If the momnth was august do new Date(2019, 7,1) instead of new Date(2019, 8,1)

//Start date for querying
const START_DATE = new Date(2018, 8,1);
//End date for querying
const END_DATE = new Date(2021, 8,1);

//Curreny day querying
var currentDay = START_DATE;

(async () => {
	// constants
	
	// storage for set of tweets
	const tweetSet = [];

	while(true){
		//Stops looping when the target date is reached
		if(currentDay.getFullYear() == END_DATE.getFullYear()  && currentDay.getMonth() == END_DATE.getMonth() && currentDay.getDate() == END_DATE.getDate()){
			break;
		}
		
		//Converts the day into a string
		let curStartDay = new Date(currentDay);
		let curStartDayStr = curStartDay.getFullYear() + "-" +(curStartDay.getMonth() + 1) + "-" + curStartDay.getDate();
		//end day is the next day because it [startDay,endDay)
		let curEndDay = new Date(curStartDay.getFullYear(), curStartDay.getMonth(), curStartDay.getDate() + 1);
		let curEndDayStr = curEndDay.getFullYear() + "-" + (curEndDay.getMonth() + 1) + "-" + curEndDay.getDate();

		//The url for retriving the tweets for the day
		const PAGE_URL = PAGE_URL_START + curEndDayStr + PAGE_URL_MID + curStartDayStr + PAGE_URL_END;

		//Amount of tweets attempting topull
		const TWEET_LIMIT = 10;

		// initialize browser with page and viewport
		const browser = await puppeteer.launch({
			headless: false,
		});
		const page = await browser.newPage();
		await page.setViewport({
			width: 1000,
			height: 800,
		});
		await page.goto(PAGE_URL, {
			waitUntil: "networkidle0",
		});

		// grab tweets until a) we cannot physically anymore or b) we hit the limit that we need
		let canMove = true;
		let i = 0;
		while (canMove && i < TWEET_LIMIT) {
			// press j to go to next tweet
			await page.keyboard.press("j", { delay: 200 });

			const data = await page.evaluate(() => {
				const MIN_TWEET_SPLIT_LENGTH = 5;
				// get the tweet that is focused
				const tweet = document.querySelector(
					"article[data-focusvisible-polyfill=true]",
				);

				if (!tweet) {
					console.error("Hit non-tweet object, skipping");
					return null;
				}
				//Gets the div for the date of the tweet
				const dateDiv = tweet.querySelector("time");
				//Makes a date obj for the date
				const dateObj = new Date(dateDiv.innerHTML);
				//Converts the date obj to string
				let date = dateObj.getFullYear() + "/" + (dateObj.getMonth() + 1) + "/" + dateObj.getDate();

				// remove interaction counts because those mess with the innerText retrieval
				const interactions = document.querySelector("div[role=group]");
				if (interactions) interactions.remove();

				// split up tweet text into lines
				let rawTweet = tweet && tweet.innerText;
				rawTweet = rawTweet.split("\n");

				// if the split tweet text does not contain the required number of splits, abort
				if (rawTweet < MIN_TWEET_SPLIT_LENGTH) return null;

				// return tweet and date if found
				return {
					Tweet: rawTweet.slice(4).join("\n"),
				 	Date: date
				};
			});
			
			//If the obj looked inside is not a tweet(null) then continue
			if(data == null){
				continue;
			}
			//The index currently being checked for duplicates
			let checkIndex= tweetSet[tweetSet.length - 1];
			//While it's in the array
			while(checkIndex >= 0){
				//If its a different date that means it's checked all the tweets for that day
				if(data.Date != tweetSet[checkIndex].Date){
					break;
				} 
				//If the tweet is the same then it's captured the last tweet in the feed
				if(data.Tweet == tweetSet[checkIndex].Tweet){
					console.log("Captured last tweet in feed. (Hit duplicate)");
					canMove = false;
					break;
				}
				//Goes to the next index to check
				checkIndex--;
			}
			//If hasn't reached the last tweet then add the tweet to the tweet array
			if(canMove){
				tweetSet[tweetSet.length] = data;
				i++;
			}
		}
		await browser.close();
		//Goes to the next day for tweet collection
		currentDay = new Date(currentDay.getFullYear(), currentDay.getMonth(), currentDay.getDate() + 1);
		console.log("Days Left: " + ((END_DATE - currentDay) / 60/60/24/1000))
	}

	//Writes the data into a csv
	const createCsvWriter = require('csv-writer').createObjectCsvWriter;
	const csvWriter = createCsvWriter({
		path: 'C:/Users/jesse/Documents/Stuff/CodeThings/ACM/ACM_StockData/scraper/tweetstest.csv',
		header: [
		  {id: 'Tweet', title: 'Tweet'},
		  {id: 'Date', title: 'Date'},
		]
	  });
	csvWriter.writeRecords(tweetSet).then(()=> console.log('The CSV file was written successfully'));

})();
