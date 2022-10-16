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
next_id = 152

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


@app.get("/getPokemonsByType/{type}")
async def getPokemonsByType(type):
    return await db_manager.getPokemonsByType(type)


@app.delete("/deleteOwnership/")
async def deleteOwnership(pokemonName, trainerName):
    return await db_manager.deleteOwnership(pokemonName, trainerName)


@app.put("/evolve/")
async def evolve(pokemonName, trainerName):
    return await db_manager.evolve(pokemonName, trainerName)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
