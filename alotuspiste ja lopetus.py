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

#tehdään random maali ja aloituspiste
all_airports = airports()
goal_num = random.randint(0,len(all_airports)-1)
start_num = random.randint(0,len(all_airports)-1)
goal_airport = all_airports[goal_num]['ident']
start_airport = all_airports[start_num]['ident']

print(start_airport)
print(goal_airport)