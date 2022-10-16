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

def test_add_trainer():
    pass

def test_add_new_pokemon_to_db():
    response = client.post("/addPokemon/yanma")
    assert response.status_code == 200
    response = client.get("/getTypes/yanma")
    assert response.status_code == 200
    types = response.json()
    assert len(types) == 2, f"Duplicate types found for yanma...."
    assert "bug" in types and "flying" in types 
    

def test_delete_ownership():
    pass

def test_evolv():
    pass

