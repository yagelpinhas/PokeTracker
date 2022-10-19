
from fastapi import FastAPI
import uvicorn
import routers.pokemons as pokemons
import routers.trainers as trainers

app = FastAPI()
app.include_router(pokemons.router)
app.include_router(trainers.router)


@app.get('/')
def root():
    return "PokeTracker Server is now running..."


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
