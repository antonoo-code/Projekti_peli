import random
from contextlib import nullcontext

import mysql.connector
from geopy import distance

from peli import npc_connective_flight

connection = mysql.connector.connect(
    port=3306, #oletusarvo ei pakollinen.
    host="127.0.0.1", #oletusarvo ei pakollinen.
    database = 'projektipeli',
    user='projekti',
    password='sala',
    autocommit=True
)

def airports():
    sql = ("SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND type = 'large_airport' limit 20;")
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

all_airports = airports()
goal_num = random.randint(0,len(all_airports)-1)
start_num = random.randint(0,len(all_airports)-1)
goal_airport = all_airports[goal_num]['ident']
start_airport = all_airports[start_num]['ident']

def airport_data(icao):
    sql = ("SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def update_location(icao, p_range): #lokaation muutos pelissä
    sql = ("UPDATE game SET location = %s, player_range = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range))

# Etäisyys kentästä toiseen

def airports_in_range(icao, airports, player_range):
    in_range = []
    for airport in airports:
        distance = calculate_distance(icao, airport['ident'])
        if distance <= player_range and not distance == 0:
            in_range.append(airport)
    return in_range

def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance(start['latitude_deg'], start['longitude_deg']),
(end['latitude_deg'], end['longitude_deg']))

airports = airports_in_range(current_airport, all_airports, player_range)
print(f"Voit lentää seuraaville lentokentille: {len(airports)}")
if len(airports) == 0:
    print("Pakko ladata lentokone.")
elif input("Heitä noppaa :"):

else:
    print(f"Lentokentät: ")
    for airport in airports:
        airport_distance = calculate_distance(current_airport, airport['ident'])
        print(f"{airport['nimi']}, icao: {airport['ident']}, distance: {airport_distance:0f}km")

# Kysy seuraavaa kohdetta
destination = input("Mihin mennään seuraavaksi?: ")
selected_distance = calculate_distance(current_airport, destination)
player_range = selected_distance
update_location(destination, player_range, game_id)
current_airport = destination

# Noppafunktio

def throw_dice():
    throw_dice = random.randint(1, 6)
    print(throw_dice)

throw_dice()

# Nopanheitto lentokentällä

penalties = ["Salamanisku", "Passi", "Wrongcountry", "NPC", "Fatigue", "Football", "Raffle"]

Salamanisku = print("Salama iski koneen akkuun, sait akun täyteen ja 200km ylimääräistä lentoa!")
Passi = print("Jäit tullissa kiinni vanhasta passista, sinun on palattava takaisin lähtömaahan.")
Wrongcountry = print("Lentokone lähti lentoon, mutta sen oli tehtävä pakkolasku Atlantille.")
NPC = print("Huomasit kilpailijan koneen, voittaaksesi kisan kävit vetäisemässä hänen latausjohtonsa irti, hän joutuu odottamaan ylimääräiset 12 tuntia.")
Fatigue = print("Olet väsynyt, joudut käyttämään ylimääräiset 12 tuntia nukkumiseen.")
Football = print("Televisiosta tulee lempi jalkapalloseurasi ottelu, katsot sen loppuun ja myöhästyt lennoltasi.")
Raffle = print("Voitit lentokentän pika-arvonnan ja saat uuden lentokoneen käyttöösi, voit jatkaa lentämistä heti.")


def penalty_game():
    in airports:
    input("Heitetään noppaa: ")
    print(throw_dice)
        random.shuffle(penalties)
    print(penalties)
    if Salamanisku:
        player_range = 600
    if Passi:
        update_location = start_airport
    if Wrongcountry:
        game_over = True
    if NPC:
        npc_connective_flight = null
    if Fatigue:
        current_airport = current_airport
    if Football:
        current_airport = current_airport
    if Raffle:
        current_airport = update_location

















