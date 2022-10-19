from fastapi import APIRouter
import poke_db_manger

router = APIRouter()
db_manager = poke_db_manger.PokeDBManeger()

router = APIRouter(
    prefix="/trainers",
    tags=["trainers"]
)



@router.get("/")
async def findOwners(pokemon = None):
    if pokemon is None:
        return "no query parametrs givven ('pokemon')"
    return await db_manager.findOwners(pokemon)


@router.post("/")
async def addNewTrainer(name = None, town = None):
    if name is None or town is None:
        return "one or more query parametrs missing ('name', 'town')"
    return await db_manager.addNewTrainer(name, town)


@router.post("/pokemon")
async def addOwnership(pokemon = None, trainer = None):
     if pokemon is None or trainer is None:
        return "one or more query parametrs missing ('name', 'town')"
     return await db_manager.addNewOwnership(trainer, pokemon)

@router.delete("/pokemon")
async def deleteOwnership(pokemon, trainer):
    return await db_manager.deleteOwnership(pokemon, trainer)