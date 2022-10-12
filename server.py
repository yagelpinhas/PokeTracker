from tkinter.tix import Tree
from fastapi import FastAPI , status ,  HTTPException , Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import requests
import pymysql 
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poketracker",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

app = FastAPI()

@app.get('/')
def root():
   print("Server is now running...")

def getPokemonIdByName(pokemonName):
    try:
        with connection.cursor() as cursor:
            query=f'SELECT id from pokemons where name ="{pokemonName}"'
            cursor.execute(query)
            result = cursor.fetchall()
            pokemonID=result[0]["id"]
            return pokemonID
    except TypeError as e:
        print(e)

def addTypeToPokemon(type,pokemonName):
    try:
        with connection.cursor() as cursor:
            pokemonID=getPokemonIdByName(pokemonName)
            query = f'INSERT INTO pokemon_types (pokeID,type) VALUES({pokemonID},"{type}");'
            cursor.execute(query)
            connection.commit()
    except TypeError as e:
        print(e)

def getTypesByPokemonId(pokemonId):
    try:
        with connection.cursor() as cursor:
            query=f'SELECT type from pokemon_types where pokeID={pokemonId}'
            cursor.execute(query)
            result = cursor.fetchall()
            types = list(map(lambda x: x["type"], result))
            return types
    except TypeError as e:
        print(e)

@app.get("/getTypes/{pokemonName}")
async def getTypes(pokemonName):
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonName}")
    pokemon=res.json()
    types=[]
    for obj in pokemon["types"]:
        types.append(obj["type"]["name"])
    for type in types:
        addTypeToPokemon(type,pokemonName)
    pokemonID=getPokemonIdByName(pokemonName)
    types = getTypesByPokemonId(pokemonID)
    print(types)

@app.get("/findOwners/{pokemonName}")    
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
@app.get("/findPokemons/{trainerName}")
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

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8065,reload=True)