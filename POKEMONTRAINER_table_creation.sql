use poketracker;
CREATE TABLE pokemon_trainer(
    pokeID INT,
    trainer_name VARCHAR(50),
    FOREIGN KEY(pokeID) REFERENCES pokemons(id),
    FOREIGN KEY(trainer_name) REFERENCES trainers(name)
);






