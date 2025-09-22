from geopy import distance
import mysql.connector
import random

connection = mysql.connector.connect(
    port=3306, #oletusarvo ei pakollinen.
    host="127.0.0.1", #oletusarvo ei pakollinen.
    database = 'projektipeli',
    user='projekti',
    password='sala',
    autocommit=True)

def airports():
    sql = ("SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND type = 'large_airport' limit 20;")
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

#tehdään random maali ja aloituspiste
all_airports = airports()
goal_num = random.randint(0,len(all_airports)-1)
start_num = random.randint(0,len(all_airports)-1)
goal_airport = all_airports[goal_num]['ident']
start_airport = all_airports[start_num]['ident']

def airport_data(icao): # lentokentän info
    sql = ("SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def update_location(icao, p_range): #lokaation muutos pelissä
    sql = ("UPDATE game SET location = %s, player_range = %s")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range))

current_airport = start_airport

game_running = True
while game_running:
    # get current airport info
    airport = airport_data(current_airport)
    # show game status
    print(f'Olet nyt {airport['name']}.')
    print(f'sinulla on {player_range:.0f}kilometriä rangea.')
    # kysytään haluuako ladata, heittää noppaa tai lentää.
    #kerrotaan kuinka lähellä on maalia ja kuinka lähellä npc on

    destination = input('Enter destination icao: ') #liikutaan seuraavaan pisteeseen ja päivitetään lokaatio
    selected_distance = calculate_distance(current_airport, destination)
    player_range -= selected_distance
    update_location(destination, player_range)
    current_airport = destination