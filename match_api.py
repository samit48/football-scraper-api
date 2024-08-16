from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import datetime


app = Flask(__name__)


#function to get the json from the web scraper
def fetch_matchs(date_value):

    url = f"https://fbref.com/en/matches/{date_value}"

    print()
    print(url)
    

        
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
    print()
    print(all_matches)
    print()
    return all_matches



@app.route("/matches", methods=["GET"])
def get_matches():
    date = request.args.get("date", None)

    if date:
        date_value = date
    else:
        date_today = datetime.datetime.now()
        date_value = date_today.strftime("%Y-%m-%d")

    print(date_value)
    matches = fetch_matchs(date_value)
    return jsonify(matches)


if __name__ == "__main__":
    app.run(debug = True)
