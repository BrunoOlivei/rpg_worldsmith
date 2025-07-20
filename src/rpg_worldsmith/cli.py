import typer
from rpg_worldsmith.services.preference_collector import PreferenceCollector
from rpg_worldsmith.services.world_generator import WorldGenerator

app = typer.Typer()


@app.command()
def world():
    collector = PreferenceCollector()
    preferences = collector.collect_preferences()
    generator = WorldGenerator(preferences)
    generator.generate()


def main():
    typer.run(world)
