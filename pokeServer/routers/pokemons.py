from fastapi import APIRouter
import poke_db_manger

router = APIRouter()
db_manager = poke_db_manger.PokeDBManeger()

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
        return "no query parametrs givven ('trainer' or 'type')"


@router.post("/{pokemonName}")
async def addPokemon(pokemonName):
    return await db_manager.addPokemon(pokemonName)

@router.get("/types/{pokemonName}")
async def getTypes(pokemonName):
    return await db_manager.getTypes(pokemonName)

@router.put("/evolve")
async def evolve(pokemon, trainer):
    return await db_manager.evolve(pokemon, trainer)
