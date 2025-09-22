


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