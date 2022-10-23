# PokeTracker

A simple server side, using the free Poke api and local database using mySql.


# API:

- GET   /   (senity)

## Pokemons:
- #### GET   /pokemons ####      
- - query parameters: trainer, type
- - (list pokemons by trainer or by type) 

- #### POST  /pokemons/{pokemonName} #### 
- - (add new pokemon to DB)

- #### PUT   /pokemons/evolve#### 
- - query parameters: trainer, pokemon
- - (evolve pokemon of a trainer, if available)

- #### GET   /pokemons/types/{pokemonName}####
- - (list the types of a pokemon) 


## trainers:
- #### GET   /trainers      ####
- - query parameters: pokemon
- - (list all trainers that have <PkemonName>) 

- #### POST  /trainers####
- - query parameters: name, town
- - (add a new trainer) 


- #### POST   /trainers/pokemon####
- - query parameters: trainer, pokemon
- - (add a new pokemon to a trainer) 

- #### DELETE   /trainers/pokemon ####
- - query parameters: trainer, pokemon
- - (delete an ownership between pokemon and a trainer) 

