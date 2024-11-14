import typer

app = typer.Typer()

@app.command()
def main():
    welcome_scene()
    query = homeostat_scene()
    cards = draw_scene(query)
    interpretation = interpretation_scene(query, cards)
    farewell_scene()