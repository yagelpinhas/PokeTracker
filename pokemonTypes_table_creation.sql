use poketracker;
CREATE TABLE pokemon_types(
    pokeID INT,
    type VARCHAR(50),
    FOREIGN KEY(pokeID) REFERENCES pokemons(id),
);
