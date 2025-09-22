
current_airport = start_airport

game_running = True
while game_running:
    # get current airport info
    airport = airport_data(current_airport)

    # todo kerrotaan kuinka lähellä on maalia ja kuinka lähellä npc on
    print(f'Olet nyt lentokentällä:  {airport['name']}.')
    print(f'sinulla on {player_range:.0f}kilometriä rangea.')
    # kysytään haluuako ladata, heittää noppaa tai lentää.
    do = input('haluatko ladata (lataa), heittää noppaa(heita) tai lentää(lenna)')
    if do == 'lataa':

    elif do == 'heita':
        throw_dice()
    elif do == 'lenna':
        # todo anna lento vaihtoehdot
        destination = input('Enter destination icao: ') #liikutaan seuraavaan pisteeseen ja päivitetään lokaatio
        selected_distance = calculate_distance(current_airport, destination)
        player_range -= selected_distance
        update_location(destination, player_range)
        current_airport = destination