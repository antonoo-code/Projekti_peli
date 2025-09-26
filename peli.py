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
    """Hakee tietokannasta haltuut lentokentät ja niistä kaikki oleelliset tiedot."""
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result



def distance_from_airport_distance(x): #Anton
    return x[1]

def get_npc_connective_flight_options(in_range_ports, goal): #Anton
    """Etsii npc:lle kolme parasta vaihtoehtoa kaikista kentistä jotka rangessa"""
    airport_distances = []
    for airport in in_range_ports:
        range = calculate_distance(airport[0], goal)  
        if range != 0:
            total_distance = airport[1]+ int(range)
            airport_distances.append([airport[0], total_distance]) # airport[1]+range on matka maaliin lähtöpisteestä.
    airports_with_shortest_distance = sorted(airport_distances, key=distance_from_airport_distance)[:3]
    return airports_with_shortest_distance    


def get_npc_destination_icao(npc_flight_options): #Anton
    """Tää funktio palauttaa npc-pelaajan lehtovaihtoehdoista satunnaisesti yhden kentän icao-koodin"""
    random_index =random.randint(0,len(npc_flight_options)-1)
    return npc_flight_options[random_index][0]


def calculate_distance(current, target): #Anton
    """Laskee etäisyyden nykyisen ja mahdollisen seuraavan kentän väliltä."""
    start = airport_data(current)
    end = airport_data(target)
    return distance.distance([start['latitude_deg'], start['longitude_deg']], [end['latitude_deg'], end['longitude_deg']]).kilometers


def update_location(icao, p_range): #lokaation muutos pelissä
    """Päivittää pelaajan sijainnin ja rangen?"""
    sql = ("UPDATE game SET location = %s, player_range = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range))

def player_airport_range_calc(icao, airport_list, player_range): #Anton
    """Kertoo mitkä kentät ovat pelaajan rangen sisällä."""
    in_range = []
    for airport in airport_list:
        range = calculate_distance(icao, airport['ident'])
        if range <= player_range and range != 0:
            in_range.append([airport['name'], airport['ident'], int(range)])
    return in_range


def npc_airport_range_calc(npc_icao, airport_list, npc_range): #Anton
    """Kertoo mitkä kentät ovat npc:n rangen sisällä."""
    in_range = []
    for airport in airport_list:
        range = calculate_distance(npc_icao, airport['ident'])
        if range <= npc_range and range != 0:
            in_range.append([airport['ident'], int(range)])
    return in_range

def get_airport_name(icao): #Anton
    """Etsii halutun kentän nimen käyttäen icaota."""
    sql = (f"SELECT name FROM airport WHERE ident = '{icao}'")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result ['name']

def get_list_function(x):   
    """Syötetään x paikalle nopan saatu silmäluku ja funktio kertoo mikä tapahtuuma siitä tulee."""
    penalties = ["Salamanisku", "Passi", "Wrongcountry", "NPC", "Fatigue", "Football", "Raffle"]
    funktion = penalties[x]
    return funktion

def throw_dice(): #noppa
    """heittää noppaa 1-6."""
    throw_dice = random.randint(0, 6)
    return throw_dice

def what_happens(tulos, pelaajan_range):
    """Kertoo mitä millakin nopan silmäluuvulla tapahtuu."""
    if tulos == "Raffle":
        #Mitä pelin koodissa tapahtuu
        print("Voitit lentokentän pika-arvonnan ja saat uuden lentokoneen käyttöösi, voit jatkaa lentämistä heti.")
        return
    elif tulos == "Football":
        #Mitä pelin koodissa tapahtuu
        print("Televisiosta tulee lempi jalkapalloseurasi ottelu, katsot sen loppuun ja myöhästyt lennoltasi.")



def airport_data(icao): #lentokentän tiedot
    """Hakee tietokannasta kaikki tiedot identillä."""
    sql = ("SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def print_player_in_range_ports(in_range_ports): #Anton
    """Antaa tulostuksen vaihtoehdoista mihin voi lentää."""
    print_content = []
    for airport in in_range_ports:
        port_name = airport_data(airport[0])['name']
        print_content.append(f'Lentokentän koodi: {airport[0]}, Lentokentän nimi: {port_name}, Lentokentälle on {airport[1]} kilometriä matkaa.')
    print(print_content)

def main_npc_flight_fuunction(current_location,all_ports, npcrange, goalport): #Anton
    """Tärkein funktio laskee mille kentälle npc liikkuu seuraavaksi."""
    destination = get_npc_destination_icao(get_npc_connective_flight_options(npc_airport_range_calc(current_location, all_ports, npcrange ),goalport))
    return destination

all_airports = airports()
goal_num = random.randint(0,len(all_airports)-1)
start_num = random.randint(0,len(all_airports)-1)
goal_airport = all_airports[goal_num]['ident']
start_airport = all_airports[start_num]['ident']




current_airport = start_airport
npc_current_airport = start_airport
end_airport = airport_data(goal_airport)
player_turns = 0
npc_turns = 0
player_range = 600
npc_range_1 = 600
print(f'Määränpääsi {end_airport['name']} ja etäisyys sinne on {calculate_distance(start_airport, goal_airport):.0f} kilometriä')
game_running = True
while game_running:
    player_turns = player_turns + 1
    if npc_current_airport != goal_airport:
        npc_turns = npc_turns + 1 #todo lisätään vuoroja vaan siihen asti että npc maalissa
    airport = airport_data(current_airport)


    # kysytään haluuako ladata, heittää noppaa tai lentää laitoin while nii ei tuu väärää kometoa
    do_run = True
    while do_run:
        print(f'Sinun sijaintisi on: {get_airport_name(current_airport)} matkaa maaliin on: {calculate_distance(current_airport, goal_airport)} kilometriä, sekä sinulla on rangea jäljellä {player_range} kilometriä.') #Anton
        print(f'Möttösen sijainti on: {get_airport_name(npc_current_airport)} ja matkaa maaliin on: {calculate_distance(npc_current_airport, goal_airport)} kilometriä.') #Anton
        do = input('haluatko ladata (lataa), heittää noppaa(heita) tai lentää(lenna): ')
        if do == 'lataa':
            print('latasit akun täyteen')
            player_range = 600
            do_run = False
        elif do == 'heita':
            get_list_function(throw_dice())
            
            do_run = False
        elif do == 'lenna':
            player_flight_options = player_airport_range_calc(current_airport, all_airports, player_range)
            for i in player_flight_options:
                print(i)
            destination = input('Enter destination icao: ') #liikutaan seuraavaan pisteeseen ja päivitetään lokaatio
            selected_distance = calculate_distance(current_airport, destination)
            player_range -= selected_distance
            update_location(destination, player_range)
            current_airport = destination
            do_run = False
        else:
            print('annoit väärän komennon')
        if npc_range_1 > 500: #jos npc range yli 500 npc lentää seuraavaavalle kentälle. #Anton
            npc_destination = main_npc_flight_fuunction(npc_current_airport,all_airports, npc_range_1, goal_airport)  
            npc_selected_distance = calculate_distance(npc_current_airport, npc_destination)
            npc_range_1  -= npc_selected_distance
            update_location(npc_destination, npc_range_1)
            npc_current_airport = npc_destination
            do_run = False
        else: # jos range alle 500 npc valitsee latauksen.
            npc_range_1 = 1000
            do_run = False #Anton
    
    
    if current_airport == goal_airport or npc_current_airport == goal_airport:
        game_running = False


if player_turns == npc_turns:
    print('tasapeli')
elif player_turns > npc_turns:
    print('voitit')
elif player_turns < npc_turns:
    print('hävisit')