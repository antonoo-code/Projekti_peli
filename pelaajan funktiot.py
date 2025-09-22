import random

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
(end['latitude_deg'], end['longitude_deg'])).km

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
destination = input("Mihin mennään seuraavaksi: ")
selected_distance = calculate_distance(current_airport, destination)
player_range = selected_distance
update_location(destination, player_range, game_id)
current_airport = destination

# Noppafunktio

def throw_dice():
    throw_dice = random.randint(1, 6)
    print(throw_dice)

throw_dice()









