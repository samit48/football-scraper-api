# football-scraper-api

This code is a Flask web application that provides an API to fetch and return football match data from a website (fbref.com). The API serves match information for the top five European football leagues: Premier League, La Liga, Serie A, Bundesliga, and Ligue 1. Here's a breakdown of how it works:

Imports and Flask App Initialization:

The script imports necessary modules, including Flask for creating the web application, requests for making HTTP requests, BeautifulSoup for parsing HTML, json for working with JSON data, and datetime for handling date operations.
A Flask app is initialized using Flask(__name__).
Function to Fetch Matches:

The fetch_matchs function takes a date as input and constructs a URL for the fbref.com matches page for that date.
It sends an HTTP GET request to the URL and parses the HTML response using BeautifulSoup.
The function searches for tables containing match data (stats_table sortable min_width) and extracts relevant information for each match, including the home team, away team, time, game week, and score.
The matches are filtered by league, ensuring only matches from the top leagues are included.
The extracted match data is stored in a dictionary with the league name as the key and a list of matches as the value.
API Endpoint:

The /matches endpoint is defined with a GET method.
It accepts an optional date parameter from the query string. If no date is provided, the current date is used.
The fetch_matchs function is called with the specified or current date, and the resulting match data is returned as a JSON response.
Running the App:

The application is run in debug mode, allowing for live reloading and detailed error messages during development.
This setup allows users to retrieve football match data by making a GET request to the /matches endpoint, optionally specifying a date. The API then scrapes the relevant data from the fbref.com website and returns it in JSON format.
