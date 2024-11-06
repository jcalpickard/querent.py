import typer
from dataclass import dataclass

@dataclass
class Card:
    """A card"""
    is_major: bool
    is_court: bool
    has_figure: bool
    number: bool
    name: bool
    suit: bool
    # Etc etc etc TBA

@dataclass
class Session:
   """Everything we want to save in humus the session"""
    query : str
    result : [Card]
    interpretations : [str]

class QuerentHumusClient:
    """A thing that's responsible for indexing everything in humus so that we can get it back in ways that are useful"""
    def save_session(session : Session):
        """Save the query, drawn cards, interpretation, in whatever manner we decide"""
        pass

    def get_existing_interpretations(query : str, card : Card) -> [str]:
        """Returns accumulated 'meanings' for the drawn cards and this query"""
        pass

def welcome_scene():
    """Here we do the scene setting"""
    pass

def homeostat_scene():
    """Here we do the 'query elicitation' and refinement"""
    query = ???
    return query


def draw_scene(query):
    """Here we guide the user in drawing cards, and receive their responses"""
    card1 = ???
    card2 = ???
    card3 = ???
    return [card1, card2, card3]

def interpretation_scene(query, result, previous_interpretations):
    """Here we take the user through the process of interpretation of the reading,
    with reference to their query, and to relevant previous interpretations"""
    interpretation = ???
    return interpretation

def farewell_scene():
    """Here we transition out of the querent session, giving the user time to reflect and say goodbye"""

app = typer.Typer()

@app.command()
def run():
    welcome_scene()
    query = homeostat_scene()
    result = draw_scene(query)
    humus = QuerentHumusClient()
    previous_interpretaions = []
    for card in result:
        previous_interpretations[card] = humus.get_existing_interpretations(query, card)
    interpretation = interpretation_scene(query, result, previous_interpretations)
    session = Session(query, result, interpretation)
    humus.save_session(session)
    farewell_scene()

if __name__ == "__main__":
    app()
