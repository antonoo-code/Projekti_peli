import mysql.connector

from peli import get_airport_name, calculate_distance, goal_airport, npc_current_airport, player_flight_options

connection = mysql.connector.connect(
    port=3306, #oletusarvo ei pakollinen.
    host="127.0.0.1", #oletusarvo ei pakollinen.
    database = 'projektipeli',
    user='projekti',
    password='sala',
    autocommit=True)


# Aloittaa pelin

def create_game(p_range, cur_airport, p_name):
    sql = f"""INSERT INTO game (player_range, location, screen_name) VALUES (%s, %s, %s)"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (p_range, cur_airport, p_name))
    connection.commit()
    cursor.close()
    g_id = cursor.lastrowid
    return g_id


# Peliasetukset

print("Sitten ku olet valmis aloittamaan")
player_name = input("Anna pelaaja nimi: ")



# Koodi rivien siivousta ja pelikokemuksen parantamista

# 159 - 161 rivien siivousta
while game_running:
    player_turns += 1
    if npc_current_airport != goal_airport:
        npc_turns += 1


# 167 - 169 rivistä siivosin koodit ja paransin ulkonäköä pelissä.
while do_run:
    goal_name = get_airport_name(goal_airport)
    goal_distance = calculate_distance(current_airport, goal_airport)
    npc_location = get_airport_name(npc_current_airport)
    npc_distance_to_goal = calculate_distance(npc_current_airport, goal_airport)

    print(f"Sinun sijaintisi on: {get_airport_name(current_airport)}")
    print(f"Etäisyys maaliin: {goal_distance:.0f} km")
    print(f"Rangea jäljellä: {player_range:.0f} km")
    print(f"Möttösen sijainti on: {npc_location}")
    print(f"Etäisyys maaliin: {npc_distance_to_goal:.0f} km")


# 171 rivi siivous
if not player_flight_options:

# 186 - 187 rivi, joka kerta ku valitsee lentokohteen, niin
# näkyy myös maalilentokenttä ja sen icao koodi, helpotakseen pelajaa.
elif do == 'lenna':
    print(f"Maali on:", goal_name, goal_airport)