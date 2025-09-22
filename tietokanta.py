import mysql.connector

connection = mysql.connector.connect(
    port=3306, #oletusarvo ei pakollinen.
    host="127.0.0.1", #oletusarvo ei pakollinen.
    database = 'projektipeli',
    user='projekti',
    password='sala',
    autocommit=True)



def create_game(p_range, cur_airport, p_name):
    sql = f"""INSERT INTO game (player_range, location, screen_name) VALUES (%s, %s, %s)"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (p_range, cur_airport, p_name))
    connection.commit()
    cursor.close()
    g_id = cursor.lastrowid
    return g_id