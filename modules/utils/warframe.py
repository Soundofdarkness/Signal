
import requests

import json


def get_worldstate():
    url = 'http://content.warframe.com/dynamic/worldState.php'
    ws = requests.get(url).json()
    return ws


def id_to_relay(ident:str):
    if "Pluto" in ident:
        name = "Orcus Relay"

    elif "Mercury" in ident:
        name = "Larunda Relay"

    elif "Saturn" in ident:
        name = "Kronia Relay"

    return name


def item_to_name(item:str):
    item_name = item.split("/")
    item_name = item_name[-1]
    string = "/Lotus/Language/Items/" + item_name + "Name"
    file = open("cache\\warframe\\Languages.json", encoding='utf-8')
    language = json.load(file)
    name = language[string]
    return name


def string_to_name(string:str):
    file = open("cache\\warframe\\Languages.json", encoding='utf-8')
    data = json.load(file)
    name = data[string]
    return name


def faction_to_name(faction:str):
    if "INFESTATION" in faction:
        name = "Infestation"
    elif "GRINEER" in faction:
        name = "Grineer"
    elif "CORPUS" in faction:
        name = "Corpus"
    return name


def mission_to_name(string: str):
    name = string.split("_")
    name = name[-1]
    return name


def difficulty_parse(dif: str):
    num1 = dif[3]
    num2 = dif[4]
    num = str(num1) + str(num2) + "%"


def node_to_name(node: str):
    file = open('cache\\warframe\\solNodes.json')
    data = json.load(file)
    name = data['nodes'][node]['value']
    return name
