import json
import pymysql 
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poketracker",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
the_file = open("poke_data.json")
poke_data = json.load(the_file)

def insertPokemonData(id,name,type,height,weight):
    try:
        with connection.cursor() as cursor:
            query = f'INSERT INTO pokemons (id,name,type,height,weight) VALUES({id},"{name}","{type}",{height},{weight});'
            cursor.execute(query)
            connection.commit()
    except TypeError as e:
        print(e)

def insertTrainerData(name,town):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT * FROM trainers WHERE name ="{name}";'
            cursor.execute(query)
            result = cursor.fetchall()
            if(len(result)==0):
                query = f'INSERT INTO trainers (name,town) VALUES("{name}","{town}");'
                cursor.execute(query)
                connection.commit()
    except TypeError as e:
        print(e)

def insertOwnership(pokeID,trainer_name):
    try:
        with connection.cursor() as cursor:
            query = f'INSERT INTO pokemon_trainer (pokeID,trainer_name) VALUES({pokeID},"{trainer_name}");'
            cursor.execute(query)
            connection.commit()
    except TypeError as e:
        print(e)

def insertData():
    for pokemon in poke_data:
        insertPokemonData(pokemon["id"],pokemon["name"],pokemon["type"],pokemon["height"],pokemon["weight"])
        for trainer in pokemon["ownedBy"]:
            insertTrainerData(trainer["name"],trainer["town"])
            insertOwnership(pokemon["id"],trainer["name"])

insertData()



