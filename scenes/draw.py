import typer
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime

# this DrawScene mediates between computational logics and material reality
# basically a "fancy form of data entry"

# ...
# [?] How to maintain the querent's reflective state 
# while transitioning to more structured input?
# [?] Should the homeostat's variety measures influence the card input path?
# ...

@dataclass
class InputState:
    """Tracks the state of card input interaction."""
#   variety: Variety  # inherited from homeostat module
    depth_level: int
    timestamp: datetime
    environmental_context: dict

class CardSuit(Enum):
    MAJOR = "major"
    CUPS = "cups"
    SWORDS = "swords"
    WANDS = "wands"
    PENTACLES = "pentacles"

@dataclass
class PlacedCard:
    """Represents a card that has been physically placed in reading space."""
    # core physical aspects; space and time
    # captures both the spatial and temporal aspects of the act of drawing

    position: int                       # order in which card was placed
    timestamp: datetime                 # when card "settled" into position
    initial_recognition: str            # how card was first recognised/named
    formal_name: Optional[str] = None   # formal card name (can be added later)
    is_reversed: Optional[bool] = None  # physical orientation
    notes: Optional[str] = None         # any other observations

@dataclass
class Card:
    suit: CardSuit
    name: str
    number: Optional[int] = None
    is_reversed: bool = False
    first_impression: Optional[str] = None
    timestamp: datetime = None

@dataclass
class DrawSession:
    """Manages the card-drawing session."""
    cards: List[PlacedCard] = field(default_factory=list)
    current_position: int = 0

    def add_card(self, initial_recognition: str) -> PlacedCard:
        card = PlacedCard(
            position=self.current_position,
            timestamp=datetime.now(),
            initial_recognition=initial_recognition,
            formal_name=None,
            is_reversed=False,
            notes=None
        )
        self.cards.append(card)
        self.current_position += 1
        return card

class CardInput:
    def __init__(self):
        self.current_card = None
        self.first_impression = None
        self.depth_level = 1
        self.timestamp = None

class DrawScene:
    def __init__(self, query: str):
        self.query = query
        self.session = DrawSession()
        self.cards_drawn = []
    
    def guide_drawing(self):
        print("\nTake a moment to shuffle the deck.")
        input("Press Enter when you're ready to begin...")
        print(f"\nConsidering your prompt: {self.query}")
        print("\nLet's draw three cards...")
        
        for position in range(3):
            self._guide_single_draw(position + 1)
            
        return self.cards_drawn
    
    def _guide_single_draw(self, position):
        print(f"\n--- CARD {position} ---")
        input("Press Enter when you're ready to draw... ")
        
        card = self._collect_card_input()
        self.cards_drawn.append(card)

    def _collect_card_input(self):
        initial_recognition = input("What card presents itself? ").strip()   # phrasing of this could use some work

        # default to upright when Enter key is pressed
        orientation = input("Orientation (Enter=upright, r=reversed): ").strip().lower()
        is_reversed = True if orientation == 'r' else False

        # optional first impression
        impression = input("First impression (optional, press Enter to skip): ").strip()

        return {
            'recognition': initial_recognition,
            'reversed': is_reversed,
            'impression': impression if impression else None,
            'timestamp': datetime.now()
        }

def draw_session(query):
    scene = DrawScene(query)

    print("Card Drawing")

    drawn_cards = scene.guide_drawing()

    print("\nYour reading:")
    for i, card in enumerate(drawn_cards, 1):
        orientation = "reversed" if card['reversed'] else "upright"
        print(f"\nCARD {i}: {card['recognition']} ({orientation})")
        if card['impression']:
            print(f"First impression: {card['impression']}")
            
    return drawn_cards

if __name__ == "__main__":
    typer.run(draw_session)