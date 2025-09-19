from geopy import distance
import mysql.connector

connection = mysql.connector.connect(
    port=3306, #oletusarvo ei pakollinen.
    host="127.0.0.1", #oletusarvo ei pakollinen.
    database = 'flight_game', 
    user='root',
    password='Rekolammas123',
    autocommit=True)

def airports():
    sql = ("SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND type = 'large_airport' limit 20;")
    cursor = connection.cursor(dictionary = True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

print(f'{airports()}')







