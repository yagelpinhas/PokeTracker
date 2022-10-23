from fastapi import APIRouter, HTTPException
import poke_db_manager

router = APIRouter()
db_manager = poke_db_manager.PokeDBManeger()

router = APIRouter(
    prefix="/pokemons",
    tags=["pokemons"]
)



@router.get("/")
async def getPokemonsBy(trainer = None, type = None):
    if trainer is not None:
        return await db_manager.findPokemons(trainer)
    elif type is not None:
        return await db_manager.getPokemonsByType(type)
    else:
        raise HTTPException(status_code=400, detail="no query parametrs givven ('trainer' or 'type')")


@router.post("/{pokemonName}")
async def addPokemon(pokemonName):
    return await db_manager.addPokemon(pokemonName)

@router.get("/types/{pokemonName}")
async def getTypes(pokemonName):
    return await db_manager.getTypes(pokemonName)

@router.put("/evolve")
async def evolve(pokemon, trainer):
    if pokemon is None or trainer is None:
        raise HTTPException(status_code=400, detail="one or more query parametrs missing ('name', 'town')")
    return await db_manager.evolve(pokemon, trainer)
