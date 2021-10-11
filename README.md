# uk-politics-tweet-scraper

A set of scripts for pulling in the latest tweets from UK politicians and dumping into a GCP bucket for later analysis.

* data_collection - Contains scripts for scraping. Twitter API and GCP credentials are required. The initial_scrape script is carried out initially as it grabs a large number of tweets. The tweets_update function in scrape_functions only scrapes the tweets that have been made since the previous scrape (via tweet ID).
* notebooks - contains exploratory data analysis on the tweets.