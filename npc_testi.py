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




"""def airports():
    sql = ("SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND type = 'large_airport' limit 20;")
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
selected_ports = airports()

def get_airport_name(icao):
    sql = ("SELECT name FROM airport WHERE ident = {icao}")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result


def airport_data(icao):
    sql = ("SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def calculate_distance(current, target):
    start = airport_data(current)
    end = airport_data(target)
    return distance.distance([start['latitude_deg'], start['longitude_deg']], [end['latitude_deg'], end['longitude_deg']]).kilometers
    

def npc_airport_range_calc(npc_icao, airport_list, npc_range):
    in_range = []
    for airport in airport_list:
        range = calculate_distance(npc_icao, airport['ident'])
        if range <= npc_range and range != 0:
            in_range.append([airport['ident'], int(range)])
    return in_range

   #tällä voidaan kutsua mitä tahansa airport_datasta  airport_data(airport[0])['xxx']    
def print_npc_in_range_ports(in_range_ports):
    print_content = []
    for airport in in_range_ports:
        port_name = airport_data(airport[0])['name']
        print_content.append(f'Lentokentän koodi: {airport[0]}, Lentokentän nimi: {port_name}, Lentokentälle on {airport[1]} kilometriä matkaa.')
    


def distance_from_airport_distance(x):
    return x[1]


def get_npc_connective_flight_options(in_range_ports):  #kun kutsuu niin goal_airport parametriksi goal kohdalle.
    airport_distances = []
    for airport in in_range_ports:
        range = calculate_distance(airport[0], 'EDDM')   # EDDM on maalin ident
        if range != 0:
            total_distance = airport[1]+ int(range)
            airport_distances.append([airport[0], total_distance]) # airport[1]+range on matka maaliin lähtöpisteestä.
    airports_with_shortest_distance = sorted(airport_distances, key=distance_from_airport_distance)[:3]
    return airports_with_shortest_distance          

def get_npc_destination_icao(npc_flight_options):
   
    random_index =random.randint(0,len(npc_flight_options)-1)
    return npc_flight_options[random_index][0]
    


#while- luppi järjestys 
#nykyinen sijainti
#in range tyhjänä
#calc haku
#in range täytettynä
#lentokentän valinta
#nykyinen sijainti
#in range tyhjänä tyhjennetään in_range= []



selected_ports = airports()

first_flight_list = npc_airport_range_calc('ESSA' , selected_ports, 1500 )

npc_options = get_npc_connective_flight_options(first_flight_list)
print(npc_options)


npc_destination = get_npc_connective_flight_options(npc_airport_range_ca

def main_npc_flight_fuunction(current_location,all_ports, npcrange): #Anton
   
    get_npc_destination_icao(get_npc_connective_flight_options(npc_airport_range_calc(current_location, all_ports, npcrange )))


nowloc= 'EFHK'

print(f'{main_npc_flight_fuunction(nowloc, selected_ports, 2000)}')