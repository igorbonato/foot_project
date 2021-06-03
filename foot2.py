import requests
from bs4 import BeautifulSoup
import json
from pandas import json_normalize

# headers for be a navv
headers = {'User-Agent': 'Mozilla/5.0'}

players = ['messi', 'cristiano', 'neymar',
           'kane', 'cavani', 'dybala', 'haaland',
           'mbappe', 'ibrahimovic', 'luis suarez',
           'hazard', 'ozil', 'de bruyne', 'lukaku',
           'rashford', 'quagliarella', 'ribery', 'robben',
           'gerard moreno', 'dzeko', 'van persie', 'mane',
           'immobile', 'benzema', 'giroud', 'salah', 'aspas',
           'muller', 'morata', 'vardy', 'bruno fernandes',
           'heung-min', 'lacazette', 'aubameyang', 'depay',
           'ben yedder', 'yilmaz', 'di maria', 'tadic', 'bale',
           'kramaric', 'sancho', 'higuain', 'payet', 'luis muriel',
           'lautaro', 'insigne', 'belotti', 'zapata', 'mertens',
           'wayne rooney', 'coutinho', 'alexis sanchez', 'ilicic',
           'milik', 'icardi', 'werner', 'raul jimenez', 'danny ings',
           'sterling', 'aguero', 'carlos tevez', 'firmino', 'david silva',
           'huntelaar']

url = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query="
urls = []
url_player = []
base = "http://www.transfermarkt.com/"


def get_stats(urls):
    """ entra na url de cada jogador e coleta todos stats """
    players = {"Players": []}

    for url in urls:
        i = 0
        object_response = None
        while not object_response and i < 5:
            try:
                object_response = requests.get(url, headers=headers)
            except:
                i += 1
                pass

        page = BeautifulSoup(object_response.content, 'html.parser')
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
        player["Minutes"] = int(
            ((minutes[1].text).replace(".", "").replace("'", "")))
        player["Goals per game"] = round(player["Goals"] / player["Games"], 3)
        player["Goals + Assists"] = (player["Goals"] + player["Assists"])
        player["Goals per minutes"] = round(
            player["Goals"] / player["Minutes"], 3)
        player["Assists per game"] = round(
            player["Assists"] / player["Games"], 3)
        player["G&A per game"] = round(
            (player["Goals"] + player["Assists"]) / player["Games"], 3)
        player["G&A per minutes"] = round(
            (player["Goals"] + player["Assists"]) / player["Minutes"], 3)

        players["Players"].append(player)
    return players


def read_json(great_dict, filename, excel=False):
    """ função pega dict com stats dos jogadores e cria um arquivo json ou excel facultativo """
    file_json = filename+".json"
    with open(file_json, 'w') as outfile:
        json.dump(great_dict, outfile, indent=4)
    if excel:
        conv_xml(file_json, filename+"x.xlsx")


def conv_xml(file_json, filename):
    """ cria um xml a partir do json """
    with open(file_json, 'r') as infile:
        d = json.load(infile)
        normed = json_normalize(d, record_path=["Players"])
        normed.to_excel(filename, index=False, sheet_name="Stats Players")


# looping de busca dos jogadores no site

for player in players:
    k = 0
    i = None
    while not i and k < 5:
        try:
            i = requests.get(url+player, headers=headers)
        except:
            k += 1
            pass

    urls.append(i)
    player_page = BeautifulSoup(i.content, features="html.parser")
    try:
        player_num = player_page.find(
            "a", {"class": "spielprofil_tooltip"})["href"]
    except TypeError:
        print(f'O jogador {player} não foi encontrado')
        continue

    p = player_num.split("/")
    new_url = base + p[1] + "/leistungsdaten/spieler/" + \
        p[-1]+"/plus/0?saison=ges"
    url_player.append(new_url)


a = get_stats(url_player)
read_json(a, "dataplayers2.0")
