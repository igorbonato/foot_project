import requests
from bs4 import BeautifulSoup

# headers for be a nav
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# url site
site = "https://www.transfermarkt.com/lionel-messi/leistungsdaten/spieler/28003/plus/0?saison=ges"

# download page
objeto_response = requests.get(site, headers=headers)

page = BeautifulSoup(objeto_response.content, 'html.parser')
players = {}
player = {}

tag_player = page.find("h1", {"itemprop": "name"})
player["Name"] = tag_player.text
games = page.find_all("td", {"class": "zentriert"})
player["Games"] = int(games[0].text)
goals = page.find_all("td", {"class": "zentriert"})
player["Goals"] = int(goals[1].text)
assists = page.find_all("td", {"class": "zentriert"})
player["Assists"] = int(assists[2].text)
minutes = page.find_all("td", {"class": "rechts"})
player["Minutes"] = int(((minutes[1].text).replace(".", "").replace("'", "")))
player["Goals per game"] = round(player["Goals"] / player["Games"], 3)
player["Goals per minutes"] = round(player["Goals"] / player["Minutes"], 3)
player["Assists per game"] = round(player["Assists"] / player["Games"], 3)
player["G&A per game"] = round((player["Goals"] + player["Assists"]) / player["Games"], 3)
player["G&A per minutes"] = round((player["Goals"] + player["Assists"]) / player["Minutes"], 3)
print(player)
