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


@app.get("/getTypes/{pokemonName}")
async def getTypes(pokemonName):
    return await db_manager.getTypes(pokemonName)


@app.get("/findOwners/{pokemonName}")
async def findOwners(pokemonName):
    return await db_manager.findOwners(pokemonName)


@app.get("/findPokemons/{trainerName}")
async def findPokemons(trainerName):
    return await db_manager.findPokemons(trainerName)


@app.post("/addNewTrainer/")
async def addNewTrainer(name, town):
    return await db_manager.addNewTrainer(name, town)


@app.post("/addPokemon/{pokemonName}")
async def addPokemon(pokemonName):
    return await db_manager.addPokemon(pokemonName)


@app.post("/addOwnership/")
async def addPokemon(pokemon, trainer):
    return await db_manager.addNewOwnership(trainer, pokemon)

@app.get("/getPokemonsByType/{type}")
async def getPokemonsByType(type):
    return await db_manager.getPokemonsByType(type)


@app.delete("/deleteOwnership/")
async def deleteOwnership(pokemon, trainer):
    return await db_manager.deleteOwnership(pokemon, trainer)


@app.put("/evolve/")
async def evolve(pokemon, trainer):
    return await db_manager.evolve(pokemon, trainer)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
