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
selected_ports = airports()

def airport_data(icao):
    sql = ("SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def calculate_distance(current, target):
    start = airport_data(current)
    end = airport_data(target)
    return distance.distance(start['latitude_deg'], start['longitude_deg']), (end['latitude_deg'], end['longitude_deg']).km


def npc_airport_range_calc(icao, Airport_funktio, npc_range):
    in_range = []
    for Airport_funktio in Airport_funktio:
        range = calculate_distance(icao, Airport_funktio['ident'])
        if range <= npc_range and not range == 0:
            in_range.append(Airport_funktio)
        return range

print(f'{npc_airport_range_calc('ESSA' , selected_ports, 1500 )}')