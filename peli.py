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


def airports(): #haetaan lentokentät mitä käytetään
    sql = ("SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND type = 'large_airport' limit 20;")
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
selected_ports = airports()

all_airports = airports()

#otetaan alkupiste ja maali
goal_num = random.randint(0,len(all_airports)-1)
start_num = random.randint(0,len(all_airports)-1)
goal_airport = all_airports[goal_num]['ident']
start_airport = all_airports[start_num]['ident']

def npc_connective_flight(in_range_ports, goal):  #kun kutsuu niin goal_airport parametriksi goal kohdalle.
    airport_distances = []
    for airport in in_range_ports:
        range = calculate_distance(airport[0], goal)   # EDDM on maalin ident
        if range != 0:
            total_distance = airport[1]+ int(range)
            airport_distances.append([airport[0], total_distance]) # airport[1]+range on matka maaliin lähtöpisteestä.
    airports_with_shortest_distance = sorted(airport_distances, key=lambda x: x[1])[:3]
    return airports_with_shortest_distance    


def calculate_distance(current, target):
    start = airport_data(current)
    end = airport_data(target)
    return distance.distance([start['latitude_deg'], start['longitude_deg']], [end['latitude_deg'], end['longitude_deg']]).kilometers


def update_location(icao, p_range): #lokaation muutos pelissä
    sql = ("UPDATE game SET location = %s, player_range = %s")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range))

def player_airport_range_calc(icao, airport_list, player_range): #lentokentät pelaajan rangella
    in_range = []
    for airport in airport_list:
        range = calculate_distance(icao, airport['ident'])
        if range <= player_range and range != 0:
            in_range.append([airport['ident'], int(range)])
    return in_range


def npc_airport_range_calc(npc_icao, airport_list, npc_range): #lentokentät npc:n rangella
    in_range = []
    for airport in airport_list:
        range = calculate_distance(npc_icao, airport['ident'])
        if range <= npc_range and range != 0:
            in_range.append([airport['ident'], int(range)])
    return in_range

def throw_dice(): #noppa
    throw_dice = random.randint(1, 6)
    print(throw_dice)

def airport_data(icao): #lentokentän tiedot
    sql = ("SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def print_player_in_range_ports(in_range_ports): #lentokentät rangella printti
    print_content = []
    for airport in in_range_ports:
        port_name = airport_data(airport[0])['name']
        print_content.append(f'Lentokentän koodi: {airport[0]}, Lentokentän nimi: {port_name}, Lentokentälle on {airport[1]} kilometriä matkaa.')
    print(print_content)


current_airport = start_airport
player_turns = 0
npc_turns = 0


game_running = True
while game_running:
    player_turns = player_turns + 1
    npc_turns = npc_turns + 1
    # get current airport info
    airport = airport_data(current_airport)

    # todo kerrotaan kuinka lähellä on maalia ja kuinka lähellä npc on
    print(f'Olet nyt lentokentällä:  {airport['name']}.')
    print(f'sinulla on {player_range:.0f}kilometriä rangea.')
    # kysytään haluuako ladata, heittää noppaa tai lentää laitoin while nii ei tuu väärää kometoa
    do_run = True
    while do_run:
        do = input('haluatko ladata (lataa), heittää noppaa(heita) tai lentää(lenna)')
        if do == 'lataa':
            print('latasit akun täyteen')
            player_range = 600
            do_run = False
        elif do == 'heita':
            #anna muuttujat mitä nopan silmäluvuilla tulee
            print(f'heitit silmäluvun {throw_dice()}')
            do_run = False
        elif do == 'lenna':
            # anna lento vaihtoehdot
            destination = input('Enter destination icao: ') #liikutaan seuraavaan pisteeseen ja päivitetään lokaatio
            selected_distance = calculate_distance(current_airport, destination)
            player_range -= selected_distance
            update_location(destination, player_range)
            current_airport = destination
            do_run = False
        else:
            print('annoit väärän komennon')