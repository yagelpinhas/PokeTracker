import pymysql
import requests


class PokeDBManeger:

    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db="poketracker",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )

    def getPokemonIdByName(self, pokemonName):
        try:
            with self.connection.cursor() as cursor:
                query = f'SELECT id from pokemons where name ="{pokemonName}"'
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) == 0:
                    return "No such pokemon name in the database"
                pokemonID = result[0]["id"]
                return pokemonID
        except TypeError as e:
            print(e)

    def addTypeToPokemon(self, type, pokemonID):
        try:
            with self.connection.cursor() as cursor:
                query = f'SELECT * FROM pokemon_types WHERE pokeID={pokemonID} AND type="{type}");'
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) > 0:
                    return
                query = f'INSERT INTO pokemon_types (pokeID,type) VALUES({pokemonID},"{type}");'
                cursor.execute(query)
                self.connection.commit()
        except TypeError as e:
            print(e)

    def getTypesByPokemonId(self, pokemonId):
        try:
            with self.connection.cursor() as cursor:
                query = f'SELECT type from pokemon_types where pokeID={pokemonId}'
                cursor.execute(query)
                result = cursor.fetchall()
                types = list(map(lambda x: x["type"], result))
                return types
        except TypeError as e:
            print(e)

    async def getTypesFromApi(pokemonName):
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonName}")
        if res.status_code == 404:
            return "there is no such pokemon in the api"
        pokemon = res.json()
        types = []
        for obj in pokemon["types"]:
            types.append(obj["type"]["name"])
        return types

    async def getTypes(self, pokemonName):
        pokemonID = self.getPokemonIdByName(pokemonName)
        types = await self.getTypesFromApi(pokemonName)
        for type in types:
            self.addTypeToPokemon(type, pokemonID)
        types = self.getTypesByPokemonId(pokemonID)
        return types

    async def findOwners(self, pokemonName):
        try:
            with self.connection.cursor() as cursor:
                query = f'SELECT trainer_name FROM pokemon_trainer,pokemons WHERE pokemon_trainer.pokeID=pokemons.id AND pokemons.name="{pokemonName}"'
                cursor.execute(query)
                result = cursor.fetchall()
                names_only = list(map(lambda x: x["trainer_name"], result))
                return names_only
        except TypeError as e:
            print(e)

    async def findPokemons(self, trainerName):
        try:
            with self.connection.cursor() as cursor:
                query = f'SELECT pokemons.name as name FROM pokemons,trainers,pokemon_trainer WHERE pokemon_trainer.trainer_name=trainers.name AND pokemons.id=pokemon_trainer.pokeID AND trainers.name="{trainerName}"'
                cursor.execute(query)
                result = cursor.fetchall()
                names_only = list(map(lambda x: x["name"], result))
                return names_only
        except TypeError as e:
            print(e)

    async def addNewTrainer(self, name, town):
        try:
            with self.connection.cursor() as cursor:
                query = f'INSERT INTO trainers (name,town) VALUES("{name}","{town}");'
                cursor.execute(query)
                self.connection.commit()
        except TypeError as e:
            print(e)

    async def addPokemon(self, pokemonName):
        try:
            with self.connection.cursor() as cursor:
                query = f'SELECT id from pokemons where name ="{pokemonName}"'
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) > 0:
                    return "this pokemon already exists"
                res = requests.get(
                    f"https://pokeapi.co/api/v2/pokemon/{pokemonName}")
                if res.status_code == 404:
                    return "no such pokemon in the api"
                pokemon = res.json()
                global next_id
                pokemon_id = next_id
                next_id += 1
                types = await self.getTypesFromApi(pokemonName)
                height = pokemon["height"]
                weight = pokemon["weight"]
                query = f'INSERT INTO pokemons (id,name,type,height,weight) VALUES({next_id},"{pokemonName}","{types[0]}",{height},{weight})'
                cursor.execute(query)
                self.connection.commit()
                for type in types:
                    self.addTypeToPokemon(type, pokemonName)
        except TypeError as e:
            print(e)

    async def getPokemonsByType(self, type):
        try:
            with self.connection.cursor() as cursor:
                query = f'SELECT pokemons.name as name FROM pokemons,pokemon_types WHERE pokemon_types.pokeID=pokemons.id AND pokemon_types.type="{type}"'
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) == 0:
                    return "no pokemons with this type"
                names_only = list(map(lambda x: x["name"], result))
                return names_only
        except TypeError as e:
            print(e)

    def checkOwnership(self, pokemonName, trainerName):
        try:
            with self.connection.cursor() as cursor:
                pokemonId = self.getPokemonIdByName(pokemonName)
                query = f'SELECT pokeID,trainer_name FROM pokemon_trainer WHERE pokeID={pokemonId} AND trainer_name="{trainerName}"'
                cursor.execute(query)
                result = cursor.fetchall()
                return len(result) > 0
        except TypeError as e:
            print(e)

    def updateOwnership(self, trainerName, new_name, old_name):
        if self.checkOwnership(new_name, trainerName) == True:
            return "The trainer already owns the evolved pokemon"
        oldPokemonId = self.getPokemonIdByName(old_name)
        newPokemonId = self.getPokemonIdByName(new_name)
        try:
            with self.connection.cursor() as cursor:
                query = f'UPDATE pokemon_trainer SET pokeID={newPokemonId} WHERE pokeID={oldPokemonId} AND trainer_name="{trainerName}"'
                cursor.execute(query)
                self.connection.commit()
                return f"{old_name} evolved to {new_name} by {trainerName}"
        except TypeError as e:
            return e

    async def deleteOwnership(self, pokemonName, trainerName):
        if self.checkOwnership(pokemonName, trainerName) == False:
            return "Can't delete this ownership because it doesn't exist"
        try:
            with self.connection.cursor() as cursor:
                pokemonId = self.getPokemonIdByName(pokemonName)
                query = f'DELETE FROM pokemon_trainer WHERE pokeID={pokemonId} AND trainer_name="{trainerName}";'
                cursor.execute(query)
                self.connection.commit()
        except TypeError as e:
            print(e)

    async def evolve(self, pokemonName, trainerName):
        if self.checkOwnership(pokemonName, trainerName) == False:
            return "no such ownership in the database"
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonName}")
        pokemon = res.json()
        speciesUrl = pokemon["species"]["url"]
        res = requests.get(f"{speciesUrl}")
        species = res.json()
        evolution_chain_url = species["evolution_chain"]["url"]
        res = requests.get(f"{evolution_chain_url}")
        evolution_chain = res.json()
        evolution_list = evolution_chain["chain"]["evolves_to"]
        if len(evolution_list) == 0:
            return "can't evolve"
        new_name = evolution_list[0]["species"]["name"]
        if (new_name == pokemonName):
            return "can't evolve"
        return (self.updateOwnership(trainerName, new_name, pokemonName))
