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
            if len(result)==0:
                return "No such pokemon name in the database"
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
    b=5
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonName}")
    if res.status_code == 404:
        return "there is no such pokemon in the database"
    pokemon=res.json()
    a=5
    types=[]
    for obj in pokemon["types"]:
        types.append(obj["type"]["name"])
    for type in types:
        addTypeToPokemon(type,pokemonName)
    pokemonID=getPokemonIdByName(pokemonName)
    types = getTypesByPokemonId(pokemonID)
    return types

@app.get("/findOwners/{pokemonName}")    
async def findOwners(pokemonName):
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
async def findPokemons(trainerName):
    try:
        with connection.cursor() as cursor:
            query =f'SELECT pokemons.name as name FROM pokemons,trainers,pokemon_trainer WHERE pokemon_trainer.trainer_name=trainers.name AND pokemons.id=pokemon_trainer.pokeID AND trainers.name="{trainerName}"'
            cursor.execute(query)
            result = cursor.fetchall()
            names_only = list(map(lambda x: x["name"], result))
            return names_only
    except TypeError as e:
        print(e) 

@app.post("/addNewTrainer/")
async def addNewTrainer(name,town):
    try:
        with connection.cursor() as cursor:
            query = f'INSERT INTO trainers (name,town) VALUES("{name}","{town}");'
            cursor.execute(query)
            connection.commit()
    except TypeError as e:
        print(e)

@app.get("/getPokemonsByType/{type}")
async def getPokemonsByType(type):
    try:
        with connection.cursor() as cursor:
            query =f'SELECT pokemons.name as name FROM pokemons,pokemon_types WHERE pokemon_types.pokeID=pokemons.id AND pokemon_types.type="{type}"'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result)==0:
                return "no pokemons with this type"
            names_only = list(map(lambda x: x["name"], result))
            return names_only
    except TypeError as e:
        print(e)     

@app.delete("/deleteOwnership/")
async def deleteOwnership(pokemonName,trainerName):
    if checkOwnership(pokemonName,trainerName)==False:
        return "Can't delete this ownership because it doesn't exist"
    try:
        with connection.cursor() as cursor:
            pokemonId=getPokemonIdByName(pokemonName)
            query = f'DELETE FROM pokemon_trainer WHERE pokeID={pokemonId} AND trainer_name="{trainerName}";'
            cursor.execute(query)
            connection.commit()
    except TypeError as e:
        print(e)

def checkOwnership(pokemonName,trainerName):
    try:
        with connection.cursor() as cursor:
            pokemonId = getPokemonIdByName(pokemonName)
            query=f'SELECT pokeID,trainer_name FROM pokemon_trainer WHERE pokeID={pokemonId} AND trainer_name="{trainerName}"'
            cursor.execute(query)
            result = cursor.fetchall()
            return len(result)>0
    except TypeError as e:
        print(e)     

def updateOwnership(trainerName,new_name,old_name):
    oldPokemonId = getPokemonIdByName(old_name)
    newPokemonId = getPokemonIdByName(new_name)
    try:
        with connection.cursor() as cursor:
            query=f'UPDATE pokemon_trainer SET pokeID={newPokemonId} WHERE pokeID={oldPokemonId} AND trainer_name="{trainerName}"'
            cursor.execute(query)
            connection.commit()
    except TypeError as e:
        print(e)     

@app.put("/evolve/")
async def evolve(pokemonName,trainerName):
    a=5
    if checkOwnership(pokemonName,trainerName) == False:
        return "no such ownership in the database"
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonName}")
    pokemon=res.json()
    speciesUrl = pokemon["species"]["url"]
    res = requests.get(f"{speciesUrl}")
    species = res.json()
    evolution_chain_url = species["evolution_chain"]["url"]
    res = requests.get(f"{evolution_chain_url}")
    evolution_chain=res.json()
    new_name = evolution_chain["chain"]["evolves_to"][0]["species"]["name"]
    if(new_name==pokemonName):
        return "can't evolve"
    updateOwnership(trainerName,new_name,pokemonName)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8085,reload=True)