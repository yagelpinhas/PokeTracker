from posixpath import pathsep
import re
from urllib import response
import pytest

from fastapi.testclient import TestClient
import json

from server import app

client = TestClient(app)



def test_root():
    response = client.get("/")
    assert response.status_code == 200, "Test failed!, cant get main site html..."
    
def test_pokemon_type():
    response = client.get("/getTypes/eevee")
    assert response.status_code == 200
    types = response.json()
    assert len(types) == 1, f"Duplicate types found for eevee...."
    assert types[0] == "normal" 

def test_illegal_pokemon_type():
    response = client.get("/getTypes/eeveee")
    assert response.status_code == 200
    assert response.json() ==  "No such pokemon name in the database"
    

def test_get_pokemons_by_type():
    
    response = client.get("/getPokemonsByType/normal")
    assert response.status_code == 200
    pokes = response.json()
    assert 'eevee' in pokes

def test_get_pokemons_by_unknown_type():
    
    response = client.get("/getPokemonsByType/normallll")
    assert response.status_code == 200
    assert response.json() == "no pokemons with this type"

def test_get_owners():
    response = client.get("/findOwners/caterpie")
    assert response.status_code == 200
    owners = response.json()
    assert "Drasna" in owners
    response = client.get("/findOwners/charmander")
    assert response.status_code == 200
    owners = response.json()
    assert sorted(owners) == sorted(["Giovanni", "Jasmine", "Whitney"])

def test_get_owners_illegal_pokemon():
    response = client.get("/findOwners/caterpiee")
    assert response.status_code == 200
    owners = response.json()
    assert owners == "no owners found..."

def test_get_pokemon_by_owner():
    drasna_pokemons = ["wartortle", "caterpie", "beedrill", "arbok",
                       "clefairy", "wigglytuff", "persian", 
                       "growlithe", "machamp", "golem", "dodrio", 
                       "hypno", "cubone", "eevee", "kabutops"]
    response = client.get("/findPokemons/Drasna")
    assert response.status_code == 200
    pokemons = response.json()
    assert pokemons == drasna_pokemons
    
def test_get_pokemon_by_illegal_owner():
    response = client.get("/findPokemons/Drasnaaa")
    assert response.status_code == 200
    pokemons = response.json()
    assert pokemons == "no pokemons found..."

def test_add_new_ownership():
    response = client.post("/addOwnership/?pokemon=pichu&trainer=Whitney")
    assert response.status_code == 200
    assert response.json() == "added pichu to Whitney"

def test_add_new_ownership_illegal():
    response = client.post("/addOwnership/?pokemon=pichu&trainer=Whitney")
    assert response.status_code == 200
    assert response.json() == "The trainer already owns pichu"
    
def test_add_new_pokemon_to_db():
    response = client.post("/addPokemon/yanma")
    assert response.status_code == 200
    response = client.get("/getTypes/yanma")
    assert response.status_code == 200
    types = response.json()
    assert len(types) == 2, f"Duplicate types found for yanma...."
    assert "bug" in types and "flying" in types 
    
def test_add_existing_pokemon():
    response = client.post("/addPokemon/yanma")
    assert response.status_code == 200
    assert response.json() == "this pokemon already exists"

def test_add_illegal_pokemon():
    response = client.post("/addPokemon/yanmaa")
    assert response.status_code == 200
    assert response.json() == "no such pokemon in the api"

def test_delete_ownership():
    response = client.get("/findPokemons/Whitney")    
    assert response.status_code == 200
    whitney_pokemons = response.json()
    assert "venusaur" in whitney_pokemons
    response = client.delete("/deleteOwnership/?trainer=Whitney&pokemon=venusaur")
    assert response.status_code == 200
    response = client.get("/findPokemons/Whitney")    
    assert response.status_code == 200
    whitney_pokemons = response.json()
    assert "venusaur" not in whitney_pokemons



def test_delete_ownership_illegal_trainer():
    response = client.delete("/deleteOwnership/?trainer=Whitneyyy&pokemon=venusaur")
    assert response.status_code == 200
    assert response.json() == "Can't delete this ownership because it doesn't exist"

def test_delete_ownership_illegal_pokemon():
    response = client.delete("/deleteOwnership/?trainer=Whitney&pokemon=venusssssaur")
    assert response.status_code == 200
    assert response.json() == "Can't delete this ownership because it doesn't exist"

def test_cant_evolv():
    response = client.put("/evolve/?pokemon=pinsir&trainer=Whitney")
    assert response.status_code == 200
    assert response.json() == "can't evolve"
    

def test_cant_evolv_illeal_ownership():
    response = client.put("/evolve/?pokemon=spearow&trainer=Archie")
    assert response.status_code == 200
    assert response.json() == "no such ownership in the database"
  
def test_evolv():
    response = client.put("/evolve/?pokemon=oddish&trainer=Whitney")
    assert response.status_code == 200
    assert response.json() == "oddish evolved to gloom by Whitney" 

def test_evolv_duplicate():
    response = client.put("/evolve/?pokemon=oddish&trainer=Whitney")
    assert response.status_code == 200
    assert response.json() == "no such ownership in the database" 
    response = client.get("/findPokemons/Whitney")    
    assert response.status_code == 200
    whitney_pokemons = response.json()
    assert "gloom" in whitney_pokemons
    
  
def test_evolv_already_exist():
    response = client.put("/evolve/?pokemon=pikachu&trainer=Whitney")
    assert response.status_code == 200
    assert response.json() == "The trainer already owns the evolved pokemon"


