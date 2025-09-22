from geopy import distance
import mysql.connector

connection = mysql.connector.connect(
    port=3306, #oletusarvo ei pakollinen.
    host="127.0.0.1", #oletusarvo ei pakollinen.
    database = 'projektipeli', 
    user='projekti',
    password='sala',
    autocommit=True)

""""def npc_airport_data(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM airport
                  WHERE ident = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result"""

def airports():
    sql = ("SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND type = 'large_airport' limit 20;")
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def npc_airport_range_calc(Airport_funktio, npc_location):
    in_range = []
    for Airport_funktio in Airport_funktio:
        range = calculate_distance(icao, Airport_funktio['ident'])
        if range <= npc_location and not range == 0:
            in_range.append(Airport_funktio)
        return range




    cursor = connection.cursor()
    cursor.execute(airport_cordi2)
    port_cordi2 = cursor.fetchall()

    final_distance = distance.distance(port_cordi1, port_cordi2).kilometers
    return final_distance

#esimerkki funktio
"""
def airports_in_range(icao, a_ports, p_range):
    in_range = []
    for a_port in a_ports:
        dist = calculate_distance(icao, a_port['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_port)
    return in_range
"""



#Lentokenttien etäisyys laskuri 




def