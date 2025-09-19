from geopy import distance
import mysql.connector

connection = mysql.connector.connect(
    port=3306, #oletusarvo ei pakollinen.
    host="127.0.0.1", #oletusarvo ei pakollinen.
    database = 'flight_game', 
    user='root',
    password='Rekolammas123',
    autocommit=True)



<<<<<<< HEAD
=======
# valitaan euroopan lentokentät jotka ovat large ja small airport
def get_airports():
    sql = """SELECT iso_country, ident, name, type, latitude_deg, longitude_deg
FROM airport
WHERE continent = 'EU' 
AND type='large_airport' , 'small-airport'
ORDER by RAND()
LIMIT 30;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
>>>>>>> 581fb0546b83c1c0e7664c92bb1cd2ceda219182
