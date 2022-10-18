from tkinter.tix import Tree
from fastapi import FastAPI, status,  HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import requests
import pymysql
import poke_db_manger
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poketracker",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

app = FastAPI()

db_manager = poke_db_manger.PokeDBManeger()




@app.get('/')
def root():
    return "PokeTracker Server is now running..."

@app.get("/pokemons")
async def getPokemonsBy(trainer = None, type = None):
    if trainer is not None:
        return await db_manager.findPokemons(trainer)
    elif type is not None:
        return await db_manager.getPokemonsByType(type)
    else:
        return "no query parametrs givven ('trainer' or 'type')"


@app.post("/pokemons/{pokemonName}")
async def addPokemon(pokemonName):
    return await db_manager.addPokemon(pokemonName)

@app.get("/pokemons/types/{pokemonName}")
async def getTypes(pokemonName):
    return await db_manager.getTypes(pokemonName)

@app.put("pokemons/evolve")
async def evolve(pokemon, trainer):
    return await db_manager.evolve(pokemon, trainer)

@app.get("/trainers")
async def findOwners(pokemon = None):
    if pokemon is None:
        return "no query parametrs givven ('pokemon')"
    return await db_manager.findOwners(pokemon)


@app.post("/trainers")
async def addNewTrainer(name = None, town = None):
    if name is None or town is None:
        return "one or more query parametrs missing ('name', 'town')"
    return await db_manager.addNewTrainer(name, town)


@app.post("/trainers/pokemon")
async def addOwnership(pokemon = None, trainer = None):
     if pokemon is None or trainer is None:
        return "one or more query parametrs missing ('name', 'town')"
     return await db_manager.addNewOwnership(trainer, pokemon)

@app.delete("/trainers/pokemon")
async def deleteOwnership(pokemon, trainer):
    return await db_manager.deleteOwnership(pokemon, trainer)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
