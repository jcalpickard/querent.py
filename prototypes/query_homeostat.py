from typer import Typer
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from collections import deque
import random
import re
import time
import uuid # unique identifiers
from enum import Enum

# it's about guiding users into an appropriate envelope of responses and behaviours
# scaffolding a stance/mode of engagement required for a generative, co-constructive dialogue
# a lightweight way of setting expectations and a querent-system social contract
# it's a translator/mediator between the querent's initial input and
# the system's capacity to facilitate a supportive, iterative dialogue

# the variety modelling is an initial, wide-aperture stage that can
# support and accomodate a diverse range of querent states and situations
# as the interaction progresses, the system "narrows" the focus
# drawing the user into a more focused, iterative exploration of their situation

# trying to balance the need for an accomodating, responsive onboarding
# with the goal of cultivating/calibrating querent-user engagement

class SystemState(Enum):
# specific states might need more work
    SETTLING = "settling"        # initial state, establishing presence
    EXPANDING = "expanding"      # opening to broader awareness
    CONTAINING = "containing"    # providing structure/boundaries
    DWELLING = "dwelling"        # staying with particular elements
    EMERGING = "emerging"        # moving toward query formation

# when the system reaches/stays within `EMERGING` state
# for a number of interaction loops, it then activates the input module?

@dataclass
class Variety:
# modelling variety as a multidimensional construct, following the ideas of W. Ross Ashby
# assumes linear scaling (0.0-1.0) is appropriate for these measures
# normalised float values are, at least, human-interpretible and comparable/commensurable
# they're "small"
    """Measure of system-querent variety across three dimensions."""
    dispersal: float = 0.0    # degree of scatter or diffusion, looseness, spatial and conceptual spread
    intensity: float = 0.0    # emotional temperature, pressure, and energetic charge
    complexity: float = 0.0   # pattern richness and density, conceptual nesting

    def __post_init__(self):  # [?] what is `__post_init__` doing here
        # validate ranges
        for field in [self.dispersal, self.intensity, self.complexity]:
            if not 0.0 <= field <= 1.0:
                raise ValueError("Variety measures must be between 0.0 and 1.0")

    def explain(self) -> str:
        # "EXPLAIN YOURSELF"
        """Return human-legible explanation of current variety state."""
        return f"""
        Dispersal: {self.dispersal:.2f} - Spread of concepts
        Intensity: {self.intensity:.2f} - Emotional engagement
        Complexity: {self.complexity:.2f} - Pattern density
        """

# these variety measures not only determine the movements of the homeostat
# they will also modulate the "texture" of the transition to card input

@dataclass
class Session:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = field(default_factory=time.time)
    state_history: List[Tuple[SystemState, float]] = field(default_factory=list)
    variety_history: List[Variety] = field(default_factory=list)
    
    def record_state(self, state: SystemState):
        self.state_history.append((state, time.time() - self.start_time))
    
    def get_fingerprint(self) -> dict:
        return {
            'duration': time.time() - self.start_time,
            'states': len(self.state_history),
            'final_state': self.state_history[-1][0] if self.state_history else None,
            'variety_trend': [v.gathering + v.intensity for v in self.variety_history[-3:]]
        }

@dataclass
class SessionTrace:
    """Capture phenomenological evolution of interaction."""
    # a lightweight way to track the "shape" of interactions
    # while preserving privacy and a sense of transience
    variety_trajectory: List[Variety]
    state_transitions: List[Tuple[SystemState, float]]  # state and timestamp
    momentum_shifts: List[float]
    closure_window: deque  # sliding window of final interactions
    
    def capture_moment(self, variety: Variety, state: SystemState):
        """Record significant state changes and variety measures."""
        self.variety_trajectory.append(variety)
        if len(self.variety_trajectory) > self.window_size:
            self.variety_trajectory.pop(0)

@dataclass
class Environment:
    """Current conditions of the meaning-making space."""
    state: SystemState
    variety: Variety
    last_response: str
    pause_level: int = 1      # Current temporal pacing (1-5)
    depth_level: int = 1      # Current depth of engagement (1-5)
    history: List[float] = field(default_factory=list) #variety history
    momentum: float = 0.0  # rate of change
    persistence: int = 0   # duration in current state

    # [?] does temporal tracking inhere to the environment class,
    # rather than the variety assessment mechanisms?

class QueryHomeostat:
    """A homeostat for maintaining conditions conducive to query formation."""
    
    def __init__(self):
        self.environment = Environment(
            state=SystemState.SETTLING,
            variety=Variety(),
            last_response="",
            history=[],
            momentum=0.0,
            persistence=0
        )

        # pattern libraries; explicitly visible as part of ritual form (mandala-style)
        self.pause_patterns = [
            ".",
            ". .",
            ". . .",
            ". . . .",
            ". . . . ."
        ]
        
        self.containing_patterns = [
            "[ {} ]",
            "| {} |",
            "- {} -",
            "( {} )",
            "{ {} }"
        ]
        
        self.depth_patterns = [
            "{}",
            "  {}",
            "    {}",
            "      {}",
            "        {}"
        ]

#        self.temporal_patterns = {
#            # need to integrate this, but
#            "dawn": "~~~~~ The sun rises ~~~~",
#            "dusk": "~~~~~ Shadows lengthen ~~~~",
#            "night": "~~~~~ Stars wheel overhead ~~~~",
#            "threshold": "~~~~~ Between times ~~~~"
#        }

    def assess_variety(self, input_text: str) -> Variety:
        """Measure input variety through simple pattern matching."""
        variety = Variety()

        # dispersal: analyse rhythmic patterns and pacing
        variety.dispersal = self._assess_dispersal(input_text)

        # intensity: sense the "temperature" and emotional tone
        variety.intensity = self._assess_intensity(input_text)
        
        # complexity: detect conceptual density and interrelatedness
        variety.complexity = self._assess_complexity(input_text)
        
        return variety
    
    def _assess_dispersal(self, text: str) -> float:
        """Analyse rhythms and pacing to assess dispersal."""
        # core focus: rythmic scattering
        # how attention and expression are spread across the interaction space
        # more about pattern than content; fluctuations in the flow of language
        # not "messiness"; structural rhythm and its interruptions
        # irregular patterns indicate scattered attention or thought processes
        # return a normalised dispersal value between 0 and 1

        metrics = {}
    
        # 1. basic structural/rhythm measures
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
    
        if not sentences:
            return 0.0
        
        # 2. rhythmanalysis
        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        metrics['rhythmic_scatter'] = sum(
            abs(l - avg_length) for l in lengths) / (
                len(lengths) * avg_length)
        
        # 3. flow disruptions
        flow_patterns = {
            'pauses': r'[,;:]',
            'interruptions': r'[\-\(\)]',
            'trailing': r'\.\.\.|—'
        }
        disruption_markers = sum(len(re.findall(pattern, text)) 
                                 for pattern in flow_patterns.values()) / len(text)

        # 4. syntactic/structural breaks
        breaks = len(re.findall(r'\n|(?<=[.!?])\s+(?=[A-Z])', text)) / len(text)

        # combined weighting prioritising rhythm and flow
        dispersal = (
            0.5 * metrics['rhythmic_scatter'] +     # primary rhythm measure
            0.3 * disruption_markers +              # secondary flow measure
            0.2 * breaks                            # tertiary structure measure
        )
    
        return min(max(dispersal * 2.0, 0.0), 1.0)

    def _assess_intensity(self, text: str) -> float:
        """Sense the "temperature" and emotional tone to assess intensity."""
        # core focus: energetic "charge", embodied experience
        # the force or pressure behind expression
        # shifts in emotion, tone, or energy
        # from tightly wound containment to explosive release
        # return a normalised intensity value between 0 and 1

        if not text.strip():
            return 0.0

        metrics = {}
        text_len = max(len(text.split()), 1)  # avoid division by zero

        # 1. surface intensity markers
        hot_markers = {
            'exclamations': len(re.findall(r'!+|\?!|[A-Z]{3,}', text)),
            'intensifiers': len(re.findall(r'\b(very|really|absolutely|completely|totally)\b', text.lower())),
            'emphasis': len(re.findall(r'\*\*|__|!!+|\?{2,}', text)),
            'urgency': len(re.findall(r'\b(now|immediately|suddenly|always|never|must|need)\b', text.lower()))
        }

        cool_markers = {
            'qualification': len(re.findall(r'\b(perhaps|maybe|might|could|somewhat|sometimes|slowly)\b', text.lower())),
            'distance': len(re.findall(r'\b(observe|notice|sense|reflect)\b', text.lower())),
            'modulation': len(re.findall(r'[;:]|\.{2,}|—', text))
        }

        # 2. embodied references
        embodied_patterns = {
            'somatic': r'\b(feel|felt|body|heart|breath|hands|chest|stomach|gut|throat)\b',
            'personal': r'\b(I|me|my|mine)\b',
            'experiential': r'\b(sense|experience|perceive|aware)\b'
        }
        metrics['embodied'] = sum(
            len(re.findall(pattern, text.lower()))
            for pattern in embodied_patterns.values()
        ) / text_len

        # 3. repetition patterns
        words = text.lower().split()
        repetitions = len([w for i, w in enumerate(words) 
                          if i > 0 and w == words[i-1]])
        metrics['repetition'] = repetitions / text_len
        
        # 4 structural pressure
        metrics['pressure'] = (
            sum(hot_markers.values()) / text_len +
            sum(cool_markers.values()) / text_len
        )

        # 5. cross-sentence intensity shifts
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if len(sentences) > 1:
            shift_intensity = sum(1 for i in range(len(sentences)-1)
                                  if self._detect_intensity_shift(sentences[i],
                                                                  sentences[i+1]))
            metrics['shifts'] = shift_intensity / (len(sentences) - 1)
        else:
            metrics['shifts'] = 0.0

        # combined weighting
        intensity = (
            0.35 * metrics['pressure'] +    # primary structural tension
            0.30 * metrics['embodied'] +    # somatic anchoring
            0.20 * metrics['shifts'] +      # temporal dynamics
            0.15 * metrics['repetition']    # pattern emphasis
        )

        return min(max(intensity * 2.5, 0.0), 1.0)

    def _assess_complexity(self, text: str) -> float:
        """Gague conceptual density and interrelatedness to assess complexity."""
        # core focus: conceptual density, cognitive mapping
        # how ideas nest and relate to each other
        # revealed through patterns of conceptual and temporal connection
        # return a normalised complexity value between 0 and 1
        
        if not text.strip():
            return 0.0
        
        metrics = {}
        text_len = max(len(text.split()), 1)  # avoid division by zero

        # 1. connection patterns
        connection_types = {
            'comparison': r'\b(like|than|compare|compared|contrast|contrasted|similar|different)\b',
            'relation': r'\b(between|across|among|through|within)\b',
            'causation': r'\b(because|therefore|since|so)\b',
            'constrast': r'\b(but|however|although|though|yet)\b',
        }

        metrics['connections'] = sum(
            len(re.findall(pattern, text.lower()))
            for pattern in connection_types.values()
        ) / text_len

        # 2. conceptual movement
        metrics['movement'] = {
            'scale': len(re.findall(r'\b(part|whole|specific|general)\b', text.lower())),
            'time': len(re.findall(r'\b(now|then|before|after|while|during)\b', text.lower())),
            'space': len(re.findall(r'\b(here|there|between|across)\b', text.lower()))
        }

        # 3. perspectival shifts
        metrics['shifts'] = {
            'tense_shifts': len(re.findall(r'\b(had|have|will|shall|would|could|might|going to|used to)\b', text.lower())),
            'viewpoint_shifts': len(re.findall(r'\b(I|we|one|they|he|she|everyone|anyone)\b', text.lower()))
        }

        # 4. abstract language
        abstraction_patterns = {
            'concepts': r'\b(idea|theory|question|meaning|system|process|truth|principle)\b',
            'qualities': r'\b(nature|essence|character|aspect|form)\b',
            'processes': r'\b(becoming|changing|emerging|developing|flux)\b',
            'systems': r'\b(pattern|structure|relation|relationship|dynamic)\b'
        }

        metrics['abstraction'] = sum(
            len(re.findall(pattern, text.lower()))
            for pattern in abstraction_patterns.values()
        ) / text_len

        # 5. recursion/self-reference
        metrics['recursion'] = {
            'direct': len(re.findall(r'\b(this|that|these|those)\b', text.lower())),
            'self': len(re.findall(r'\b(itself|own|self)\b', text.lower())),
            'meta': len(re.findall(r'\b(think|consider|understand|question)\b', text.lower())),
            'nested': len(re.finall(r'\b(within|inside|containing|embedded)\b', text.lower())),
            'recurring': len(re.findall(r'\b(again|back|return|cycle|recur|echo)\b', text.lower()))
        }

        # combined weighting
        complexity = (
            0.30 * metrics['connections'] +                         # primary relational structure
            0.25 * sum(metrics['shifts'].values()) / text_len +     # perspective shifts
            0.25 * metrics['abstraction'] +                         # abstractions and concepts
            0.10 * metrics['movement'] +                            # conceptual movement across scales
            0.10 * sum(metrics['recursion'].values()) / text_len    # self-reference
        )

        return min(max(complexity * 2.5, 0.0), 1.0)

        # abstract language, connections, uncertainty, paradox, recursion
        # conceptual and temporal layering, abstractions, analogies
        # tense and perspective shifts, scalar change, qualifiers, time markers
        # bracketing, tangential or associative connections
        # expression of uncertainty, openness, perspective-taking

    def _detect_intensity_shift(self, sent1: str, sent2: str) -> bool:
        """Detect significant shifts in intensity between sentences."""
        # a helper function for intensity assessment
        def get_intensity_markers(text:str) -> dict:
            return {
                'hot': sum(1 for pattern in self.hot_markers 
                          if re.search(pattern, text.lower())),
                'cool': sum(1 for pattern in self.cool_markers 
                          if re.search(pattern, text.lower()))
            }
        
        m1 = get_intensity_markers(sent1)
        m2 = get_intensity_markers(sent2)

        # compare intensity profiles
        return abs((m1['hot'] - m1['cool']) - 
                   (m2['hot'] - m2['cool'])) > 1

# class VarietyRegulator:
#     """A more granular approach to variety regulation focused on emergent patterns."""

#     def __init__(self):
#         self.variety_history = deque(maxlen=5)  # deliberately limited memory
#         self.pattern_cache = {}                 # temporary pattern recognition
#         self.decay_factor = 0.15                # pattern decay reate

#     def assess_pattern(self, variety: Variety) -> Dict:
#         """Assess emergent patterns in variety measures."""
#         # record new variety state
#         self.variety_history.append(variety)

#         # detect emergent patterns
#         patterns = {
#             'oscillation': self._detect_oscillation(),
#             'convergence': self._detect_convergence(),
#             'divergence': self._detect_divergence()
#         }

#         # apply decay to existing patterns
#         for pattern in self.pattern_cache:
#             self.pattern_cache[pattern] *= (1 - self.decay_factor)
            
#         # update pattern cache with new observations
#         for pattern, strength in patterns.items():
#             if pattern not in self.pattern_cache:
#                 self.pattern_cache[pattern] = strength
#             else:
#                 # blend new and existing patterns with decay (???)
#                 self.pattern_cache[pattern] = (
#                     self.pattern_cache[pattern] * (1 - self.decay_factor) +
#                     strength * self.decay_factor
#                 )
                
#         return self.pattern_cache
    
#     def _detect_oscillation(self) -> float:
#         """Detect oscillating patterns in variety measures."""
#         if len(self.variety_history) < 3:
#             return 0.0
            
#         # look for alternating increases/decreases
#         changes = []
#         for i in range(1, len(self.variety_history)):
#             prev = self.variety_history[i-1]
#             curr = self.variety_history[i]
            
#             # calculate normalised change vectors
#             change = {
#                 'dispersal': curr.dispersal - prev.dispersal,
#                 'intensity': curr.intensity - prev.intensity,
#                 'complexity': curr.complexity - prev.complexity
#             }
#             changes.append(change)
            
#         # check for sign alternation in changes
#         oscillation = 0.0
#         for dim in ['dispersal', 'intensity', 'complexity']:
#             sign_changes = sum(
#                 1 for i in range(1, len(changes))
#                 if changes[i][dim] * changes[i-1][dim] < 0
#             )
#             oscillation += sign_changes / (len(changes) - 1)
            
#         return oscillation / 3  # normalize across dimensions

#     def _detect_convergence(self) -> float:
#         """Detect convergence patterns in variety measures."""
#         if len(self.variety_history) < 3:
#             return 0.0
            
#         # look for decreasing variance over time
#         variances = []
#         for i in range(1, len(self.variety_history)):
#             prev = self.variety_history[i-1]
#             curr = self.variety_history[i]
            
#             variance = (
#                 abs(curr.dispersal - prev.dispersal) +
#                 abs(curr.intensity - prev.intensity) +
#                 abs(curr.complexity - prev.complexity)
#             ) / 3
#             variances.append(variance)
            
#         if len(variances) < 2:
#             return 0.0
            
#         # calculate trend in variances
#         variance_trend = sum(
#             variances[i] - variances[i-1]
#             for i in range(1, len(variances))
#         ) / (len(variances) - 1)
        
#         # normalise and invert so convergence is positive (???)
#         return max(0.0, min(1.0, -variance_trend + 0.5))
        
#     def _detect_divergence(self) -> float:
#         """Detect divergence patterns in variety measures."""
#         if len(self.variety_history) < 3:
#             return 0.0
            
#         # Look for increasing differences between dimensions
#         spreads = []
#         for state in self.variety_history:
#             measures = [state.dispersal, state.intensity, state.complexity]
#             spread = max(measures) - min(measures)
#             spreads.append(spread)
            
#         if len(spreads) < 2:
#             return 0.0
            
#         # Calculate trend in dimensional spread
#         spread_trend = sum(
#             spreads[i] - spreads[i-1]
#             for i in range(1, len(spreads))
#         ) / (len(spreads) - 1)
        
#         return max(0.0, min(1.0, spread_trend))

#     def suggest_regulation(self, patterns: dict) -> tuple[float, float, float]:
#         """Suggest regulatory adjustments based on detected patterns."""
#         # base regulation on pattern strengths
#         oscillation = patterns.get('oscillation', 0.0)
#         convergence = patterns.get('convergence', 0.0)
#         divergence = patterns.get('divergence', 0.0)
        
#         # calculate suggested adjustments
#         dispersal_adj = -0.2 * oscillation + 0.1 * convergence - 0.1 * divergence
#         intensity_adj = -0.1 * oscillation - 0.2 * divergence + 0.1 * convergence
#         complexity_adj = 0.1 * convergence - 0.1 * oscillation - 0.1 * divergence
        
#         return (dispersal_adj, intensity_adj, complexity_adj)

#     def regulate_variety(self, variety: Variety) -> SystemState:
#         """Determine appropriate state based on variety measures."""
#         # update conversational history
#         self.environment.history.append(
#             (variety.dispersal + variety.intensity + variety.complexity) / 3
#         )
#         if len(self.environment.history) > 5:
#             self.environment.history.pop(0)

#         # calculate momentum (rate of change in variety)
#         self.environment.momentum = self._calculate_momentum()

#         # determine persistence in the current state
#         if self.environment.state == self.regulate_variety(variety):
#             self.environment.persistence += 1
#         else:
#             self.environment.persistence = 0

#         # use variety, momentum, and persistence to determine new state
#         if self.environment.persistence > 3 and self.environment.momentum < 0.1:
#             return SystemState.CONTAINING
#         elif variety.dispersal > 0.7:
#             return SystemState.DWELLING
#         elif variety.complexity > 0.7:
#             return SystemState.CONTAINING
#         elif variety.complexity < 0.2:
#             return SystemState.EXPANDING
#         else:
#             return SystemState.EMERGING

#     def _calculate_momentum(self) -> float:
#         """Calculate the rate of change in overall variety."""
#         if len(self.environment.history) > 1:
#             return (self.environment.history[-1] - self.environment.history[-2]) / 2
#         else:
#             return 0.0

#     def generate_response(self, input_text: str) -> str:
#         """Generate response based on input and current environment."""
#         # assess and regulate variety
#         variety = self.assess_variety(input_text)
#         new_state = self.regulate_variety(variety)
        
#         # update environment
#         self.environment.variety = variety
#         self.environment.state = new_state
        
#         # select response pattern based on state
#         if new_state == SystemState.CONTAINING:
#             response = self.containing_response(input_text)
#         elif new_state == SystemState.EXPANDING:
#             response = self.expanding_response()
#         elif new_state == SystemState.DWELLING:
#             response = self.dwelling_response(input_text)
#         elif new_state == SystemState.EMERGING:
#             response = self.emerging_response()
#         else:  # SETTLING
#             response = self.settling_response()
            
#         self.environment.last_response = response
#         return response

#     def apply_timing(self, text: str) -> str:
#         """Apply timing pattern to response."""
#         return f"{text}\n{self.pause_patterns[self.environment.pause_level - 1]}"
    
#     def apply_depth(self, text: str) -> str:
#         """Apply spatial/depth pattern to response."""
#         return self.depth_patterns[self.environment.depth_level - 1].format(text)
    
#     def containing_response(self, input_text: str) -> str:
#         """Generate containing response for high variety."""
#         # extract key phrases for reflection
#         words = input_text.split()
#         if len(words) > 5:
#             key_phrase = " ".join(words[:5]) + "..."
#         else:
#             key_phrase = input_text

#         response = self.containing_patterns[self.environment.depth_level - 1].format(key_phrase)
#         return self.apply_timing(response)
    
#     def expanding_response(self) -> str:
#         """Generate response to encourage expansion."""
#         prompts = [
#             "What else is present?",
#             "Where else does your attention move?",
#             "What other aspects feel alive?",
#             "What remains unspoken?",
#             "What other threads emerge?"
#         ]
#         return self.apply_timing(prompts[self.environment.depth_level - 1])

#     def dwelling_response(self, input_text: str) -> str:
#         """Generate response for dwelling with content."""
#         words = input_text.split()
#         if words:
#             focus_word = words[len(words)//2]  # choose middle word as focus
#             return self.apply_timing(self.apply_depth(f"staying with: {focus_word}"))
#         return self.apply_timing("staying with what's present")

#     def emerging_response(self) -> str:
#         """Generate response for query emergence."""
#         prompts = [
#             "What question begins to form?",
#             "How might this question want to be asked?",
#             "What shape does this query take?",
#             "How does this question hold your situation?",
#             "What query emerges from this exploration?"
#         ]
#         return self.apply_timing(prompts[self.environment.depth_level - 1])
    
#     def settling_response(self) -> str:
#         """Generate initial settling response."""
#         return self.apply_timing("Take a moment to settle into this space")

def demonstrate_usage():
    """Demonstrate system usage with example interaction."""
    homeostat = QueryHomeostat()
    
    # example interaction sequence
    inputs = [
        "I'm feeling uncertain about a decision I need to make",
        "EVERYTHING FEELS OVERWHELMING AND I DON'T KNOW WHAT TO DO",
        "There are so many factors to consider and I'm not sure where to begin...",
        "maybe it's about trust",
        "How do I trust my own knowing while staying open to guidance?"
    ]
    
    print("=== Query Homeostat Demonstration ===")
    print(homeostat.settling_response())
    
    for user_input in inputs:
        print(f"\nUser: {user_input}")
        response = homeostat.generate_response(user_input)
        print(f"System: {response}")
        time.sleep(2)  # simulate temporal spacing

if __name__ == "__main__":
    demonstrate_usage()