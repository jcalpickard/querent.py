import typer
from dataclasses import dataclass

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

class QueryHomeostat:
    """A thing that's responsible for the 'query refinement' process -
    deciding if a query is sufficiently 'refined' and producing prompts for further elicitation"""
    def is_stable(self, queries : [str]) -> bool:
        """Evalute if the query is 'good enough' to proceed:"""
        pass

    def prompt_for_refinement(self, queries : [str]) -> str:
        """Get a prompt to give to the user to refine the query"""  # or "regulate variety"
        pass


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
    homeostat = QueryHomeostat()
    queries = []
    #queries.append(???) #get the initial formulation of the query from the user.
    while not homeostat.is_stable(queries):
        prompt = homeostat.prompt_for_refinement(queries)
        #??? ### Show prompt to user
        #queries.append(???) #Get reformulated query back from user
    # TODO: The user explicitly consents to continue with the current formulation.
    # What happens if they say no? (Start from scratch? continue refining? Edit?)
    return queries[-1]


def draw_scene(query):
    """Here we guide the user in drawing cards, and receive their responses"""
    #card1 = ???
    #card2 = ???
    #card3 = ???
    #return [card1, card2, card3]
    pass

def interpretation_scene(query, result, previous_interpretations):
    """Here we take the user through the process of interpretation of the reading,
    with reference to their query, and to relevant previous interpretations"""
    #interpretation = ???
    #return interpretation
    pass

def farewell_scene():
    """Here we transition out of the querent session, giving the user time to reflect and say goodbye"""
    pass

app = typer.Typer()


#def run():
#    welcome
#    homeostat
#    draw
#    interpret
#    farewell

@app.command()
def run():
    welcome_scene()
    query = homeostat_scene()
    result = draw_scene(query)
    humus = QuerentHumusClient()
    previous_interpretations = []
    for card in result:
        previous_interpretations[card] = humus.get_existing_interpretations(query, card)
    interpretation = interpretation_scene(query, result, previous_interpretations)
    session = Session(query, result, interpretation)
    humus.save_session(session)
    farewell_scene()

if __name__ == "__main__":
    app()
