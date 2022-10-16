import pymysql 
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poketracker",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def getHeaviestPokemon():
    try:
        with connection.cursor() as cursor:
            query ="SELECT name, weight FROM pokemons ORDER BY weight DESC"
            cursor.execute(query)
            result = cursor.fetchall()
            return result[0]["name"]
    except TypeError as e:
        print(e)

def findByType(type):
    try:
        with connection.cursor() as cursor:
            query =f'SELECT name FROM pokemons WHERE type="{type}"'
            cursor.execute(query)
            result = cursor.fetchall()
            names_only = list(map(lambda x: x["name"], result))
            return names_only
    except TypeError as e:
        print(e)

def findOwners(pokemonName):
    try:
        with connection.cursor() as cursor:
            query =f'SELECT trainer_name FROM pokemon_trainer,pokemons WHERE pokemon_trainer.pokeID=pokemons.id AND pokemons.name="{pokemonName}"'
            cursor.execute(query)
            result = cursor.fetchall()
            names_only = list(map(lambda x: x["trainer_name"], result))
            return names_only
    except TypeError as e:
        print(e)

def findPokemons(trainerName):
    try:
        with connection.cursor() as cursor:
            query =f'SELECT pokemons.name as name FROM pokemons,trainers,pokemon_trainer WHERE pokemon_trainer.trainer_name=trainers.name AND pokemons.id=pokemon_trainer.pokeID AND trainers.name="{trainerName}"'
            cursor.execute(query)
            result = cursor.fetchall()
            names_only = list(map(lambda x: x["name"], result))
            return names_only
    except TypeError as e:
        print(e) 

