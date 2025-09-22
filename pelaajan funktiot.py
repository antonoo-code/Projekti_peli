
# Etäisyys kentästä toiseen


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
player_range -= selected_distance
update_location(destination, player_range, game_id)
current_airport = destination





