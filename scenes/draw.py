import typer
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class InputState:
    """Tracks the state of card input interaction."""
    variety: Variety  # inherited from homeostat
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
    position: int                  # order in which card was placed
    timestamp: datetime            # when card "settled" into position
    
    # recognition before categorisation
    initial_recognition: str       # how card was first recognised/named
    formal_name: Optional[str]     # formal card name (can be added later)
    
    # material properties
    is_reversed: Optional[bool]    # physical orientation
    notes: Optional[str]           # any other observations

@dataclass
class Card:
    suit: CardSuit
    name: str
    number: Optional[int] = None
    is_reversed: bool = False
    first_impression: Optional[str] = None
    timestamp: datetime = None

# ...
# [?] How to maintain the querent's reflective state 
# while transitioning to more structured input?
# [?] Should the homeostat's variety measures influence the card input path?

class CardInput:
    def __init__(self):
        self.current_card = None
        self.first_impression = None
        self.depth_level = 1
        self.timestamp = None

    def _inherit_rhythm(self, variety: Variety) -> float:
        # adapt pacing based on homeostat module's final state
        return (variety.intensity + variety.complexity) / 2
        # this might be too reductive, collapsing the measures into a single metric
        # something similar?

# ...
# thinking about transitioning into this module from
# `query_homeostat.py`
# sustaining the same reflective state that earlier module
# has cultivated or instilled in the querent
# ...

# def receive_first_card(self):
#    if self.previous_state == SystemState.EMERGING:
#        return "As your question settles, what card presents itself?"
#    return "What card do you draw?"

# minimal card input flow that maintains atmosphere
# and presents a mirrored surface of sorts
# for reflection and initial interpetations

# [?] what if the Query Homeostat is a publisher
# and the Card Input module is a subscriber?
# (pub/sub system)

# the querent interacts with the homeostat until
# achieving an `EMERGING` state
# the system then subtly transitions to card input
# through shared voice and typographic patterns
# card input inherits the homeostat's rhythm and pacing
# atmospheric continuity is key
# [?] lightweight state inheritance?

def note_card() -> Optional[PlacedCard]:

    # physical orientation becomes clear as card settles
    orientation = input("\norientation? ([enter] for upright, r for reversed) ").strip()

    card = PlacedCard(
        position=1,  # would increment in actual use
        timestamp=datetime.now(),
        initial_recognition=recognition,
        formal_name=None,  # can be filled in later
        is_reversed=orientation.lower().startswith('r'),
        notes=notes if notes else None
    )

async def get_first_impression(self) -> Optional[str]:
    """Optional elaboration based on variety measures."""
    if self.state.variety.complexity > 0.5:
        return await self.prompt_for_impression()
    return None

# [?] what is `async def` doing, here?