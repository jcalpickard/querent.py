"""
This script currently defines a standard tarot deck, and draws a predefined three-card spread.
"""

# Import the random module required to draw random cards and shuffle the deck
import random

# Import the JSON module required to convert the dictionary of interpretations to a `card_meanings.json` file
import json

# Bootstrap a simple MVP `Card` class
# TODO: Add further attributes, step-by-step, where relevant
class Card:
    def __init__(self, name, reversed=False):
        self.name = name
        self.reversed = reversed

        # Load the card meanings from the JSON file
        # [?] Could presumably load all the card names from this same JSON file as well, right?
        # [?] These are still key-value pairs, right?
        # [?] What does JSON stand for, what are its origins as a file format?
        with open("data/card_meanings.json", "r") as f:
            card_meanings = json.load(f)

        # Parse/split the meaning string into keywords and sentences
        meaning_str = card_meanings[self.name]
        self.keywords, *self.sentences = meaning_str.split('. ')
        # Remove any trailing full stops from the previous sentence
        self.sentences[-1] = self.sentences[-1].rstrip('.')

    # Added a super-simple reversal ("negation") transformation
    def meaning(self):
        if self.reversed:
            # Negate the meaning by prepending "No" or "Lacking" at random (lol)
            negated_keywords = [f"no {keyword}" if random.random() < 0.5 else f"lacking {keyword}" for keyword in self.keywords.split(', ')]
            # Join the negated keywords with commas
            negated_keywords_str = ', '.join(negated_keywords)
            # Return the negated keywords and the original sentences
            return f"{negated_keywords_str}."
        else:
            return f"{self.keywords}. {'. '.join(self.sentences)}."

# TODO: Input a seperate Dodal TdM deck (if I can be arsed)
# TODO: Rejig cards so the Major Arcana names and numbers are seperate

# Bootstrap and populate a `Deck` class, including major and minor arcana?
# Renamed the class from `TarotDeck` to `Deck`
class Deck:
    def __init__(self):
        self.major_arcana = [
        # Tweaked this so it's now generating Card objects
        # There's got to be an easier way of loading these `card_meanings`
            Card(name) for name in [
                "0 - The Fool",
                "1 - The Magician",
                "2 - The High Priestess",
                "3 - The Empress",
                "4 - The Emperor",
                "5 - The Hierophant",
                "6 - The Lovers",
                "7 - The Chariot",
                "8 - Justice",
                "9 - The Hermit",
                "10 - The Wheel of Fortune",
                "11 - Strength",
                "12 - The Hanged Man",
                "13 - Death",
                "14 - Temperance",
                "15 - The Devil",
                "16 - The Tower",
                "17 - The Star",
                "18 - The Moon",
                "19 - The Sun",
                "20 - Judgement",
                "21 - The World"
            ]
        ]

        self.suits = ["Wands", "Swords", "Cups", "Pentacles"]
        self.ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"]

        # Create a list of all the minor arcana using list comprehension (not that I know what "list comprehension" is)
        # [⎈] List comprehension flagged as a particularly "Pythonic way" to create a list; explore why this is
        # A concise way to generate a list of all possible combinations of ranks and suits?
        # The generated list was a flat list of strings (as opposed to what?), where each string represents a card in the format "rank of suit"
        # I've now rejigged this to produce a set of `Card` objects?
        # There's got to be an easier way of loading these `card_meanings`

        self.minor_arcana = [
            Card(f"{rank} of {suit}") for rank in self.ranks for suit in self.suits        
        ]

        # Combine major and minor arcana cards to create a complete `Deck`
        # It's a concatenation!
        # Earlier, `TAROT` being in all-caps meant it was a constant, intended to be invariant
        # Now, it's an object (a specific deck), an instance of the `Deck` class?

        self.deck = self.minor_arcana + self.major_arcana

    # Was keen to define a function to shuffle the deck, for ontological reasons, even if it's practically irrelevant
    # Could come in handy later, and we've already imported the random module, so might as well make use of it

    def shuffle_deck(self):
        random.shuffle(self.deck)

    # Now, the deck-class defines its own function for drawing cards from the deck, using the `random.sample()` function to avoid duplication
    # [?] What are the ontological implications of this?
    # I get the `def` here, still a little unclear about what `len` is (size/length of the `deck`?)
    # Some early confusion about whether both this draw and the print function were both required, or if there was redundancy, but no
    # TODO: It'd be good to get this error message to include the number of cards that the querent tried to draw and the size of the deck?
    # TODO: Tweak the `ValueError` message to align with the ontological nature of the error, and the principles of Bogostian carpentry
    # [?] What is the origin or significance of the `k` parameter here? Is it a maths thing?
    # [?] What are the wider implications of the `draw_cards` function being attached to the Deck, here?

    def draw_cards(self, num_cards):
        if num_cards > len(self.deck):
            raise ValueError("Deck Exhaustion Error: Attempted to draw more cards than are available. Consider the ontological implications of finitude.")
        return random.sample(self.deck, k=num_cards)
    
...

# Bootstrap a simple MVP `Spread` class
class Spread:
    def __init__(self, positions):
        self.positions = positions
        self.cards = []

    def get_position_meaning(self, position):
        return self.position[position]
    
    # Replacing/laundering `draw_cards` with `deal_cards`, and attaching this to the `Spread` class
    # Should look at the ontological implications of this distinction
    def deal_cards(self, deck, num_cards):
        self.cards = deck.draw_cards(num_cards)
        # Randomly determine whether each card in the spread is reversed or not
        # [?] Should this function stay attached to the `Spread` class, or specific `Spread` objects?
        # Need to think more about how different people handle tarot reversals
        # [?] Are there other ways to handle this? In the `Deck` class?
        # [?] What granularity of control do we need, does the querent need?
        for card in self.cards:
            if random.random() < 0.5:
                card.reversed = True

    def interpret_spread(self):
        interpretation = []
        # Okay, what the hell is the `i` doing/signifying here? It's a counter?
        for i, card in enumerate(self.cards):
            position = list(self.positions.keys())[i]
            meaning = self.positions[position]
            interpretation.append(f"{position}: {card.name} (Reversed: {card.reversed})\nInterpretation: {meaning}\nCard Meaning: {card.meaning()}\n")
        return "\n".join(interpretation)

# This now, what?, summons a new, specific deck-object for the duration of the program, that can be depopulated?
# And saves a copy of the card meanings to a seperate JSON file, as previously defined
# [?] Why are there brackets after the `TarotDeck` class?

deck = Deck()

# Create a Spread object with the desired positions and meanings
# [?] Is it normal for this to lead with the positions?
positions = {
    "ANCHOR": "The present situation, what grounds you.",
    "TIDE": "The changing influences, what's in flux.",
    "HORIZON": "The long-term outlook, what's ahead."
}
spread = Spread(positions)

# Shuffle the deck and deal three cards (or `k`?)
# Cards dealt from the specific deck-object (and not replaced), without user input
# This applies the `deal_cards` function to the `deck` object, producing dealt cards as, what, a string?
# TODO: Allow users to specify the number of cards (and reconcile with the supplied narrative scaffolding)
# [?] If I keep running the programme, will we run out of cards? Hypothesis: No, because each run spins up a new deck
# [?] When does shuffling normally take place?
deck.shuffle_deck()
spread.deal_cards(deck, 3)

# Interpret the spread
# The `interpretation` attribute is the fixed meaning of the spread position, which is fine for now
interpretation = spread.interpret_spread()
print("\nYour reading:")
print(interpretation)