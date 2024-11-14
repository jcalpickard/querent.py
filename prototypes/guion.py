from dataclasses import dataclass
from enum import StrEnum
import random
import typer
import requests # https://pypi.org/project/requests/ - to get some placeholder tarot readings from tarotapi.dev
from art import text2art # https://pypi.org/project/art/ - to print out fancy text

DEFAULT_FONT="handwriting1";

def fancy_print(text, font=DEFAULT_FONT):
    print(text2art(text, font=font));

def fancy_input(text, font=DEFAULT_FONT):
    return input(text2art(text, font=font));

class Suit(StrEnum):
    WANDS = "wands"
    SWORDS = "swords"
    PENTACLES = "pentacles"
    CUPS = "cups"

class CardNumber(StrEnum):
    ACE = "ace"
    ONE = "one"
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"
    SIX = "six"
    SEVEN = "seven"
    EIGHT = "eight"
    NINE = "nine"
    TEN = "ten"
    PAGE = "page"
    KNIGHT = "knight"
    QUEEN = "queen"
    KING = "king"

class MajorArcanaName(StrEnum):
    FOOL = 'The Fool'
    MAGICIAN = 'The Magician'
    HIGH_PRIESTESS = 'The High Priestess'
    EMPRESS = 'The Empress'
    EMPEROR = 'The Emperor'
    HIEROPHANT = 'The Hierophant'
    LOVERS = 'The Lovers'
    CHARIOT = 'The Chariot'
    FORTITUDE = 'Fortitude'
    HERMIT = 'The Hermit'
    WEEL_OF_FORTUNE = 'Wheel Of Fortune'
    JUSTICE = 'Justice'
    HANGED_MAN ='The Hanged Man'
    DEATH = 'Death'
    TEMPERANCE = 'Temperance'
    DEVIL = 'The Devil'
    TOWER = 'The Tower'
    STAR = 'The Star'
    MOON = 'The Moon'
    SUN = 'The Sun'
    JUDGMENT = 'The Last Judgment'
    WORLD = 'The World'


class Card:
    pass

@dataclass
class MajorArcana(Card):
    name : MajorArcanaName

    @property
    def display_name(self):
        return self.name.value

    @property
    def humus_path(self):
        return "/major/%s" % self.name.name

@dataclass
class MinorArcana(Card):
    suit: Suit
    number: CardNumber

    @property
    def display_name(self):
        return "%s of %s" % (self.number.value, self.suit.value)

    @property
    def humus_path(self):
        return "/minor/%s/%s" % (self.suit.name, self.number.name)

class FakeHumus:
    def __init__(self, data):
        self.data = data

    def insert(self, path, data):
        pass # Fake Humus doesn't actually persist anything.

    def get(self, path):
        # Not quite the samentics of real Humus, but for our purposes it's fine for now
        if path in self.data:
            return self.data[path]
        else:
            return []

def populated_fake_humus():
    # TODO This builds a fake humus with interpretations nabbed from tarotapi.dev. We will replace it
    # with a prepopulated real humus shortly.
    tarot = requests.get("https://tarotapi.dev/api/v1/cards").json()
    seed_data = {}
    for card_data in tarot["cards"]:
        if card_data["type"] == "major":
           card = MajorArcana(MajorArcanaName(card_data["name"]))
        elif card_data["type"] == "minor":
           suit = Suit(card_data["suit"])
           number = CardNumber(card_data["value"])
           card = MinorArcana(suit, number)
        seed_data[card.humus_path] = card_data["meaning_up"].split(";")
    return FakeHumus(seed_data)

class QuerentHumusClient:
    def __init__(self):
        self.humus = populated_fake_humus() #TODO put a real humus in here.

    """A thing that's responsible for indexing everything in humus so that we can get it back in ways that are useful"""
    def save_interpretations(self, reading: [Card], interpretation: str):
        """Save the query, drawn cards, interpretation, in whatever manner we decide"""
        for card in reading:
            self.humus.insert(card.humus_path, str)

    def get_previous_interpretations(self, reading : [Card]) -> [str]:
        """Returns accumulated 'meanings' for the drawn cards and this query"""
        interpretations = []
        for card in reading:
            interpretations += self.humus.get(card.humus_path)
        return interpretations

class QueryHomeostat:
    """A thing that's responsible for the 'query refinement' process -
    deciding if a query is sufficiently 'refined' and producing prompts for further elicitation"""
    def is_stable(self, queries : [str]) -> bool:
        """Evalute if the query is 'good enough' to proceed:"""
        # TODO Justin here is a place to add homeostat logic
        return random.random() > 0.5 # A coin toss, for now

    def prompt_for_refinement(self, queries : [str]) -> str:
        """Get a prompt to give to the user to refine the query"""  # or "regulate variety"
        # TODO Justin here is a place to add homeostat logic. return a clarifying question.
        return "aaaah, yes, but have you considered asking that in another way....?"

def welcome_scene():
    """Here we do the scene setting"""
    fancy_print("Greetings, querent", font="double")
    fancy_print("This is a welcome message which is a placeholder")

def homeostat_scene():
    """Here we do the 'query elicitation' and refinement"""
    homeostat = QueryHomeostat()
    queries = []
    fancy_print("What is your query, querent?", font="vip")
    queries.append(fancy_input("query> "))
    while not homeostat.is_stable(queries):
        prompt = homeostat.prompt_for_refinement(queries)
        fancy_print(prompt, font="tiny")
        queries.append(fancy_input("query> "))
    # TODO: The user explicitly consents to continue with the current formulation.
    # What happens if they say no? (Start from scratch? continue refining? Edit?)
    return queries[-1]

def draw_scene(query):
    """Here we guide the user in drawing cards, and receive their responses"""
    # TODO guide the user to read and input cards, and return the real ones.
    return [MajorArcana(MajorArcanaName.WORLD), MajorArcana(MajorArcanaName.FOOL), MajorArcana(MajorArcanaName.TOWER)]

def interpretation_scene(query, result, previous_interpretations):
    """Here we take the user through the process of interpretation of the reading,
    with reference to their query, and to relevant previous interpretations"""
    fancy_print("You asked: \"%s\"" % query, font="tiny")
    fancy_print("And the cards said: ")
    for card in result:
        fancy_print(" - %s" % card.display_name, font="wiggly")
    fancy_print("Some previous interpretations of these cards might suggest: ", font="tiny")
    for interpretation in random.sample(previous_interpretations, k=min(5, len(previous_interpretations))):
        fancy_print(" - %s" % interpretation, font="tiny")
    fancy_print("Do you have any reflection to add?", font="vip")
    return fancy_input("Your interpretation >")

def farewell_scene():
    """Here we transition out of the querent session, giving the user time to reflect and say goodbye"""
    fancy_print("Farewell, querent. This is from the farewell scene which is also a placeholder.")

app = typer.Typer()

@app.command()
def run():
    humus = QuerentHumusClient()
    # First welcome the user.
    welcome_scene()
    # Then elicit and refine the query
    query = homeostat_scene()
    # Then direct the user to draw cards
    result = draw_scene(query)
    # Then get the previous interpretations from humus
    previous_interpretations = humus.get_previous_interpretations(result)
    # Then guide the user in interpreting the reading
    interpretation = interpretation_scene(query, result, previous_interpretations)
    # Then save away the new interpretation in humus
    humus.save_interpretations(result, interpretation)
    # Then say goodbye.
    farewell_scene()

if __name__ == "__main__":
    app()
