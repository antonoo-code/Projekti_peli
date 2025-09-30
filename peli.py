from geopy import distance
import mysql.connector
import random

NPC_NUBER_OF_OPTIONS = 6
GAME_AIRPORT_LIMIT = 100
NPC_RANGE = 500
MAX_PLAYER_RANGE = 600
NPC_SUPERCHARGE_AMOUNT = 300
PLAYER_SUPERCHARGE_AMOUNT = 150
NPC_visited_ports = set()

#Terminaalin värjäys

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BOLD = "\033[1m"

connection = mysql.connector.connect(
    port=3306, #oletusarvo ei pakollinen.
    host="127.0.0.1", #oletusarvo ei pakollinen.
    database = 'projektipeli', 
    user='projekti',
    password='sala',
    autocommit=True)


def airports(): #haetaan lentokentät mitä käytetään
    haku = f"SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND iso_country NOT IN ('ES', 'PT', 'RU', 'ISL') AND type = 'large_airport' limit {GAME_AIRPORT_LIMIT};"
    sql = (haku)
    """Hakee tietokannasta haltuut lentokentät ja niistä kaikki oleelliset tiedot."""
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result



def distance_from_airport_distance(x): #Anton
    return x[1]

def get_npc_connective_flight_options(in_range_ports,npc_currentport, goal): #Anton
    """Etsii npc:lle N parasta vaihtoehtoa kaikista kentistä jotka rangessa"""
    airport_distances = []
    #Etsitään n määräkenttiä lähimpänä maalia.
    for airport in in_range_ports:
        plane_range = calculate_distance(airport[0], goal)  
        current_distance_to_goal = calculate_distance(npc_currentport, goal)
        if plane_range < current_distance_to_goal:
            airport_distances.append([airport[0], plane_range])
    result_connective_flights = sorted(airport_distances, key=distance_from_airport_distance)[:NPC_NUBER_OF_OPTIONS]   
    return result_connective_flights

def get_npc_destination_icao(npc_flight_options, goal): #Anton
    """Tää funktio palauttaa npc-pelaajan lehtovaihtoehdoista satunnaisesti yhden kentän icao-koodin"""
    if len(npc_flight_options) == 0:
        return None
    for airport in npc_flight_options:
        if airport[0] == goal:
            print(f'flight of victory')
            return goal #npc maalissa.
    if len(npc_flight_options)> 1:
        random_index =random.randint(0,len(npc_flight_options)-1)
    else:
        random_index = 0

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
        if airport['ident'] in NPC_visited_ports:
            continue
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
    penalties = ["Salamanisku", "Passi", "President", "Fatigue", "Raffle"]
    funktion = penalties[x]
    return funktion

def throw_dice(): #noppa
    """heittää noppaa 1-6."""
    throw_dice = random.randint(0, 4)
    return throw_dice


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
    npc_airport_range = npc_airport_range_calc(current_location, all_ports, npcrange)
    npc_connective_flight_options = get_npc_connective_flight_options(npc_airport_range, npc_current_airport, goalport)
    destination = get_npc_destination_icao(npc_connective_flight_options, goalport)
    if destination != None:
        NPC_visited_ports.add(destination)
    return destination

def get_goal_airports(start,allports): #haetaan alku lentokenttä.
    """Funktio listaa kaikista knetistä kentäntät jotka ovat kauimpana maalista joka on generoitu."""
    goal_airport_options = []
    for airport in allports:
        range = calculate_distance(airport['ident'], start)  
        goal_airport_options.append([airport['ident'], range])
    goal_airport_options = sorted(goal_airport_options, key=distance_from_airport_distance, reverse=True)[:10]
    random_index =random.randint(0,len(goal_airport_options)-1)
    random_goal_port = goal_airport_options[random_index]
    goal = random_goal_port[0]
    return goal
    


all_airports = airports()
goal_num = random.randint(0,len(all_airports)-1)
start_num = random.randint(0,len(all_airports)-1)

start_airport = all_airports[start_num]['ident']
goal_airport =  get_goal_airports(start_airport, all_airports)


current_airport = start_airport
npc_current_airport = start_airport
end_airport = airport_data(goal_airport)
player_turns = 0
npc_turns = 0
player_range = MAX_PLAYER_RANGE
npc_range_1 = NPC_RANGE
print(f'Määränpääsi {end_airport['name']}, {BLUE}{goal_airport}{RESET} ja etäisyys sinne on {calculate_distance(start_airport, goal_airport):.0f} kilometriä')
game_running = True
while game_running:
    player_turns += 1
    if npc_current_airport != goal_airport:
        npc_turns += 1  # Rohan
    #todo lisätään vuoroja vaan siihen asti että npc maalissa
    airport = airport_data(current_airport)


    # kysytään haluuako ladata, heittää noppaa tai lentää laitoin while nii ei tuu väärää kometoa
    do_run = True
    while do_run:
        if current_airport in NPC_visited_ports:
            print(f'{RED} Möttönen havaitsi jonkun romulentokoneen, seuraavan häntä. {RESET}')
            print(f' {YELLOW}Möttönen lähetti viestin: yritäppäs nyt seurata XD{RESET}')
            print(f'{GREEN}Sinun sijaintisi on:{RESET} {get_airport_name(current_airport)} matkaa maaliin on: {calculate_distance(current_airport, goal_airport):.0f} kilometriä, sekä sinulla on rangea jäljellä {player_range:.0f} kilometriä.') #Anton
        else:
            print(f'{GREEN}Sinun sijaintisi on: {RESET} {get_airport_name(current_airport)} matkaa maaliin on: {calculate_distance(current_airport, goal_airport):.0f} kilometriä, sekä sinulla on rangea jäljellä {player_range:.0f} kilometriä.')
            print(f'{YELLOW}Möttösen sijainti on:{RESET} {get_airport_name(npc_current_airport)} ja matkaa maaliin on: {calculate_distance(npc_current_airport, goal_airport):.0f} kilometriä.') #Anton
        if calculate_distance(npc_current_airport, goal_airport)+200 < calculate_distance(current_airport, goal_airport):
            print(f' {YELLOW}Möttönen lähetti sinulle viestin: Missä kaveri hinaa XDD {RESET}')
        player_flight_options = player_airport_range_calc(current_airport, all_airports, player_range)
        if player_flight_options == []:
            print('Sinulla ei ole rangea lentää minnekkään.')
            do = input(f'Haluatko ladata akun täyteen? ({BOLD}lataa{RESET}), heittää noppaa? (heita): ')
        elif player_range == MAX_PLAYER_RANGE:
            do = input('Haluatko superghargeta akkusi? (super), heittää noppaa? (heita) tai lentää? (lenna): ')
        else:
            do = input('Haluatko ladata akun täyteen? (lataa), heittää noppaa? (heita) tai lentää? (lenna): ')
        do = str.lower(do)
        if do == 'lataa':
            print('latasit akun täyteen')
            player_range = MAX_PLAYER_RANGE
            do_run = False
        elif do == 'heita':
            what_happens_options = get_list_function(throw_dice()) #Nickee
            tulos = what_happens_options
            """Kertoo mitä millakin nopan silmäluuvulla tapahtuu."""
            if tulos == "Raffle":
                print("Voitit lentokentän pika-arvonnan ja saat uuden lentokoneen käyttöösi, voit jatkaa lentämistä heti.")
                player_range = MAX_PLAYER_RANGE
            elif tulos == "President":
                print("Tasavallan presidentti on huomioinut teidän kilpailun ja myönsi sinulle uuden lentokoneen!")
                player_range = MAX_PLAYER_RANGE
            elif tulos == "Salamanisku":
                print("Salama iski koneen akkuun, sait akun täyteen ja 200km ylimääräistä lentoa!")
                player_range = MAX_PLAYER_RANGE + 200
            elif tulos == "Passi":
                print("Jäit tullissa kiinni vanhasta passista, sinun on palattava takaisin lähtömaahan.")
                current_airport = start_airport
            elif tulos == "Fatigue":
                print("Olet väsynyt, nukut pommiin ja rangesi tippui nollaan.")
                player_range = 0
            
            
            do_run = False
        elif do == 'super':
            player_range = player_range + PLAYER_SUPERCHARGE_AMOUNT
            print('Superchargesit koneesi XD')
            do_run = False
        elif do == 'lenna':
            lenna = True
            while lenna:
                player_flight_options = player_airport_range_calc(current_airport, all_airports, player_range)
                for i in player_flight_options: #Anton
                    print(f'{i[0]:<42}, {BLUE}{i[1]}{RESET}, {i[2]}km')
                print(f"{GREEN}Maali on: {end_airport['name']} ({goal_airport}){RESET}")
                destination = input(f'Syötä lentokentän {BLUE}ICAO{RESET} koodi: ') #liikutaan seuraavaan pisteeseen ja päivitetään lokaatio
                destination = str.upper(destination)
                for option in player_flight_options:
                    if option[1] == destination:
                        selected_distance = calculate_distance(current_airport, destination)
                        player_range -= selected_distance
                        update_location(destination, player_range)
                        current_airport = destination
                        do_run = False
                        lenna = False
                if lenna == True:
                    print('Syötit väärän icao koodin!!')
                                      
        else:
            print('annoit väärän komennon')
    
    
    npc_destination = main_npc_flight_fuunction(npc_current_airport,all_airports, npc_range_1, goal_airport)
    if npc_destination == None:
        npc_range_1 = npc_range_1 + NPC_SUPERCHARGE_AMOUNT
        print(f'{YELLOW}Möttönen alkoi superchargeamaan lentokonettaa XD{RESET} ')
        do_run = False
    elif npc_range_1 > NPC_RANGE/2 : #jos npc range yli 500 npc lentää seuraavaavalle kentälle. #Anton
        npc_selected_distance = calculate_distance(npc_current_airport, npc_destination)
        npc_range_1  -= npc_selected_distance
        update_location(npc_destination, npc_range_1)
        npc_current_airport = npc_destination
        do_run = False
    else: # jos range alle 500 npc valitsee latauksen.
        npc_range_1 = NPC_RANGE
        do_run = False #Anton
    
    
    if current_airport == goal_airport or npc_current_airport == goal_airport:
        game_running = False


if current_airport == goal_airport and npc_current_airport == goal_airport:
    print('Voi hemmetti tuli tasapeli!')
elif current_airport == goal_airport and npc_current_airport != goal_airport:
    print('Voitit mönttösen onnea!')
elif current_airport != goal_airport and npc_current_airport == goal_airport:
    print('hävisit yksinkertaiselle tietokone ohjelmalle häpeä!')
#KKSKSKSK #Hello