import typer
from rpg_worldsmith.services.world_creator import generate_world

app = typer.Typer()


@app.command()
def world():
    generate_world()


if __name__ == "__main__":
    app()
