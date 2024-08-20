from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import datetime


app = Flask(__name__)

# function gets specific date to get match info
# returns the matches in a dictionary from the web scraper
def fetch_matches(date_value):

    url = f"https://fbref.com/en/matches/{date_value}"    

    response = requests.get(url, headers={"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"})


    soup = BeautifulSoup(response.text, "html.parser")

    matches_table = soup.find_all('table', class_='stats_table sortable min_width')
    all_matches = {}
    top_leagues = ("Premier League", "La Liga","Serie A", "Bundesliga", "Ligue 1")

    for match_table in matches_table:
        league = match_table.find('caption').find('a').get_text(strip=True)
        league_co = match_table.find("span").get_text(strip=True)
        
        matches = []

        if league in top_leagues:
            
            # checks if its the italian Seria A
            if league == "Serie A" and league_co != "it":
                continue
            
            match_rows = match_table.find("tbody").find_all("tr")

            game_week_cell = match_rows[0].find('td', {'data-stat': 'gameweek'})
            game_week = game_week_cell.get_text(strip=True) if game_week_cell else "Null"

            for match_row in match_rows:
                # Gets all the info needed
                home_team_cell = match_row.find('td', {'data-stat': 'home_team'})
                away_team_cell = match_row.find('td', {'data-stat': 'away_team'})
                time_cell = match_row.find('td', {'data-stat': 'start_time'})
                
                score_cell = match_row.find('td', {'data-stat': 'score'})

                # Get text or default to "Null" if text is missing
                home_team = home_team_cell.find('a').get_text(strip=True) if home_team_cell and home_team_cell.find('a') else "Null"
                away_team = away_team_cell.find('a').get_text(strip=True) if away_team_cell and away_team_cell.find('a') else "Null"
                time = time_cell.get_text(strip=True) if time_cell else "Null"
                score = score_cell.get_text(strip=True) if score_cell and score_cell.get_text(strip=True) else "Null"

                home_team = home_team.encode('latin1').decode('unicode_escape')
                away_team = away_team.encode('latin1').decode('unicode_escape')

                matches.append({
                "home_team": home_team,
                "away_team": away_team,
                "time": time,
                "game_week": game_week,
                "score": score
                })

                
            if matches:
                all_matches[league] = matches

    return all_matches


# route for the /matches endpoint that responds to HTTP GET requests
@app.route("/matches", methods=["GET"])

# gets the match data through matchs and returns a json file
def get_matches():
    date = request.args.get("date", None)

    #if user doesn't input specifc date, use todays date
    if date:
        date_value = date
    else:
        date_today = datetime.datetime.now()
        date_value = date_today.strftime("%Y-%m-%d")

    matches = fetch_matches(date_value)

    return jsonify(matches)


if __name__ == "__main__":
    app.run(debug = True)
