# the welcome scene needs to:
# - establish a boundary between ordinary and divinatory spacetime
# - prime the querent to transition from passive observer to active participant
# - guide attention from external to internal awareness
# - create a "third space" that's neither purely physical nor purely imaginary/virtual
# - create a "sensory bridge" between the querent's environment and this interpretive space
# - establish conditions for "meaningful" synchronicity
# - build reciprocity between the querent and their cards
# - "slow down" temporal experience to support a depth of engagement

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# ~~ waxing moon ~~
# ~~ autumn equinox ~~
# ~~ hour of the owl ~~

@dataclass
class Threshold(Enum):
    # maybe need to think about some alternative ways of approaching this?
    APPROACHING = "approaching"
    CROSSING = "crossing"
    ARRIVED = "arrived"

@dataclass
class ThresholdMoment:
    """A record of tranisition"""
    threshold: Threshold
    # some other qualities
    timestamp: datetime = datetime.now()

# SEPERATATION STAGE; preliminal rites (separating from previous identity)
# TRANSITION STAGE; liminal rites
# INCORPORATION STAGE; postliminal rites (incorporating back into the social world)

# SPEAKING THE CURRENT PHASE OF THE MOON
# Noticing where your body makes contact with your seat. (Querent meets environment.)
# Three deliberate breaths.

# Proximal space; what's to hand, within arm's reach?
# Defining or marking sacred space with four small objects?

# The coolest surface within arm's reach.
# One card, face-down, as a threshold guardian.
# Tiny altar with what's to hand? Single object.
# Marking threshold with a single line, thread, piece of string.

# Just yes-no interactions to start?

# "What brings you to the cards today?"
# "Find something in your space that can mark a threshold. Your anchor between worlds."
# "Close your eyes for a moment."
# "What is the quietest sound you can hear?"
# "Feel the weight of the cards."
# "Are you ready to begin?"
# "We begin."
# TRANSITION TO HOMEOSTAT.