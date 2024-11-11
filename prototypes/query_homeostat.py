from dataclasses import dataclass, field
from typing import Any, List, Optional, Callable, Dict, Tuple
from collections import deque
from datetime import datetime, timedelta
import typer
import random
import re
import statistics
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

class SessionState(Enum):
    ACTIVE = "active"
    COMPLETE = "complete"
    ERROR = "error"

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
class DialogueRhythm:
    base_pause: float = 0.8         # base pause between exchanges
    thinking_pause: float = 0.3     # micro-pause for "thinking"
    char_rate: float = 0.02         # seconds per character for gradual text display

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
class VarietyThreshold:
    measure: str            # 'dispersal', 'intensity', 'complexity'
    value: float
    direction: str          # 'above', 'below'
    weight: float = 1.0

@dataclass
class Session:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.start_time = time.time()
        self.state = SessionState.ACTIVE
        self.history = []

    def record_interaction(self, input_text: str, response: str):
        self.history.append({
            'timestamp': time.time(),
            'input': input_text,
            'response': response
        })
       
    def record_state(self, state: SystemState):
        self.state_history.append((state, time.time() - self.start_time))

@dataclass
class SessionTrace:
    """Capture phenomenological evolution of interaction."""
    # a lightweight way to track the "shape" of interactions
    # while preserving privacy and a sense of transience
    # "brb gaffer-taping some lambdas to our deque"
    variety_trajectory: List[Variety]
    state_transitions: List[Tuple[SystemState, float]]  # state and timestamp
    momentum_shifts: List[float]
    
    # [!] TODO need to faff about with calibrating these patterns
    def __init__(self, window_size: int = 5):
        self.closure_window = deque(maxlen=window_size) # sliding window of interactions
        self.pattern_detectors = {
            'intensity_shift': lambda v1, v2: abs(v1.intensity - v2.intensity) > 0.3,
            'complexity_peak': lambda v: v.complexity > 0.7,
            'settling_pattern': lambda vs: all(v.dispersal < 0.4 for v in vs[-3:])
        }

    def capture_moment(self, variety: Variety, state: SystemState):
        """Motion capture (after a fashion) for meaning-making."""
        self.closure_window.append((variety, state, time.time()))

        if len(self.variety_trajectory) > self.window_size:
            recent_varieties = [v for v, _, _ in self.closure_window]
            patterns = {
                name: detector(recent_varieties) 
                for name, detector in self.pattern_detectors.items()
            }

            # detect emergent phenomena
            # this implementation is _extremely shonky_, but
            if patterns['settling pattern']:
                return 'READY_FOR_QUERY'

@dataclass
class InteractionMetrics:
    """Metrics calculated from interaction history."""
    avg_variety: float
    variety_trend: float  # positive = increasing, negative = decreasing
    state_stability: float  # how long states are maintained
    dominant_state: SystemState
    response_pattern: str  # 'stable', 'oscillating', 'evolving'

class HistoryAnalyser:
    """Analyses interaction history for patterns and insights."""
    
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.variety_history: deque = deque(maxlen=window_size)
        self.state_history: deque = deque(maxlen=window_size)
        self.timestamp_history: deque = deque(maxlen=window_size)
    
    def add_interaction(self, variety: Variety, state: SystemState, 
                       timestamp: float):
        """Record a new interaction."""
        self.variety_history.append(variety)
        self.state_history.append(state)
        self.timestamp_history.append(timestamp)

    def analyse(self) -> Optional[InteractionMetrics]:
        """Analyse recorded history and return metrics."""
        if len(self.variety_history) < 2:
            return None

        # calculate basic metrics
        variety_values = [
            (v.dispersal + v.intensity + v.complexity) / 3 
            for v in self.variety_history
        ]
        
        avg_variety = statistics.mean(variety_values)

        # calculate variety trend
        variety_trend = variety_values[-1] - variety_values[0]

        # calculate state stability
        state_changes = sum(
            1 for i in range(1, len(self.state_history))
            if self.state_history[i] != self.state_history[i-1]
        )
        state_stability = 1.0 - (state_changes / (len(self.state_history) - 1))

        # find dominant state
        state_counts = {}
        for state in self.state_history:
            state_counts[state] = state_counts.get(state, 0) + 1
        dominant_state = max(state_counts.items(), key=lambda x: x[1])[0]

        # determine response pattern
        if state_stability > 0.8:
            pattern = 'stable'
        elif self._is_oscillating():
            pattern = 'oscillating'
        else:
            pattern = 'evolving'

        return InteractionMetrics(
            avg_variety=avg_variety,
            variety_trend=variety_trend,
            state_stability=state_stability,
            dominant_state=dominant_state,
            response_pattern=pattern
        )

    def _is_oscillating(self) -> bool:
        """Detect if the system is oscillating between states."""
        if len(self.state_history) < 4:
            return False

        # check for alternating patterns
        states = list(self.state_history)
        return any(
            states[i] == states[i-2]
            for i in range(2, len(states))
        )

    def get_fingerprint(self) -> Dict:
        """Generate a unique fingerprint for the current session."""
        metrics = self.analyse()
        if not metrics:
            return {}
        
        return {
            'duration': time.time() - self.start_time,
            'states': len(self.state_history),
            'final_state': self.state_history[-1][0] if self.state_history else None,
            'dominant_state': metrics.dominant_state.value,
            'stability': f"{metrics.state_stability:.2f}",
            'pattern': metrics.response_pattern,
            'trend': 'increasing' if metrics.variety_trend > 0 else 'decreasing'
        }

@dataclass
class TransitionTrace:
    """Lightweight record of system-querent dialogue thresholds."""
    timestamp: float
    from_state: SystemState
    to_state: SystemState
    variety_snapshot: Variety
    
    def as_fingerprint(self) -> str:
        """Generate transition signature."""
        return f"{self.from_state.value}→{self.to_state.value}:{hash(self.variety_snapshot)}"

@dataclass
class Environment:
    """Current conditions of the meaning-making space."""
    state: SystemState = field(default=SystemState.SETTLING)
    variety: Variety = field(default_factory=Variety)
    last_response: str = ""

    # scalar measures
    pause_level: int = 1                                # current temporal pacing (1-5)
    depth_level: int = 1                                # current depth of engagement (1-5)

    # minimal state tracking
    history: deque = field(default_factory=lambda: deque(maxlen=5))
    momentum: float = 0.0                               # track rate of change in variety
    persistence: int = 0                                # track duration in current state

    def update(self, variety: Variety, new_state: SystemState) -> None:
        """Record new state and update environment measures."""
        # update momentum based on variety change
        prev_variety = self.history[-1] if self.history else variety
        self.momentum = self._calculate_momentum(variety, prev_variety)
        
        # update persistence
        # [?] which is, what, a counter?
        if new_state == self.state:
            self.persistence += 1
        else:
            self.persistence = 0
            
        # update core state
        self.history.append(variety)        # store entire variety object
        self.state = new_state
        self._adjust_levels(variety)

    def _calculate_momentum(self, current: Variety, previous: Variety) -> float:
        """Calculate the rate of change in overall variety."""
        if not isinstance(current, Variety) or not isinstance(previous, Variety):
            return 0.0 # return default value if types are incorrect

        current_val = (current.dispersal + current.intensity + current.complexity) / 3.0
        prev_val = (previous.dispersal + previous.intensity + previous.complexity) / 3.0
        return current_val - prev_val

    def _adjust_levels(self, variety: Variety) -> None:
        """Adjust environment levels based on variety measures."""
        # temporal pacing follows intensity
        self.pause_level = max(1, min(5, int(variety.intensity * 5) + 1))
        
        # depth follows complexity
        self.depth_level = max(1, min(5, int(variety.complexity * 5) + 1))

@dataclass
class StateTransition:
    """Represents a valid state transition with conditions and effects."""
    # enables clear documentation of valid transitions, runtime validation
    # makes the boundaries/thresholds more visible, including to querents
    # and is a hanger for transition markers, rhythmic variation, typographic noodling, etc.
    from_state: SystemState
    to_state: SystemState
    condition: Callable[[Variety], bool]
    on_transition: Optional[Callable[[], None]] = None

class StateMachine:
    """Manages system state transitions and validation."""
    
    def __init__(self):
        self._transitions: Dict[SystemState, Set[StateTransition]] = {
            state: set() for state in SystemState
        }
        self._setup_transitions()

    def _setup_transitions(self):
        """Define valid state transitions and their conditions."""

        # from SETTLING
        self.add_transition(StateTransition(
            SystemState.SETTLING,
            SystemState.EXPANDING,
            lambda v, env: v.dispersal < 0.3 and env.persistence > 2
        ))

        # from EXPANDING
        self.add_transition(StateTransition(
            SystemState.EXPANDING,
            SystemState.CONTAINING,
            lambda v, env: v.dispersal > 0.7 or v.intensity > 0.7
        ))
        
        # from CONTAINING
        self.add_transition(StateTransition(
            SystemState.CONTAINING,
            SystemState.DWELLING,
            lambda v, env: v.intensity < 0.5 and v.complexity > 0.4
        ))

        # from DWELLING
        self.add_transition(StateTransition(
            SystemState.DWELLING,
            SystemState.EMERGING,
            lambda v, env: v.complexity > 0.6 and env.persistence > 2
        ))

        # safety transitions back to SETTLING
        for state in SystemState:
            if state != SystemState.SETTLING:
                self.add_transition(StateTransition(
                    state,
                    SystemState.SETTLING,
                    lambda v, env: v.intensity > 0.9 or v.dispersal > 0.9
                ))

    def add_transition(self, transition: StateTransition):
        """Add a valid state transition."""
        self._transitions[transition.from_state].add(transition)

    def get_next_state(self, current_state: SystemState, 
                       variety: Variety, env: Environment) -> SystemState:
        """Determine the next valid state based on current conditions."""
        valid_transitions = self._transitions[current_state]

        for transition in valid_transitions:
            if transition.condition(variety, env):
                if transition.on_transition:
                    transition.on_transition()
                return transition.to_state

        return current_state  # stay in current state if no valid transitions

    def is_valid_transition(self, from_state: SystemState, 
                          to_state: SystemState) -> bool:
        """Check if a state transition is valid."""
        return any(t.to_state == to_state 
                  for t in self._transitions[from_state])

@dataclass
class SimplePatternTrace:
    """Lightweight trace of interaction patterns."""
    window_size: int = 3
    variety_window: deque = field(default_factory=lambda: deque(maxlen=3))
    
    def detect_basic_pattern(self, variety: Variety) -> Optional[str]:
        """Detect fundamental patterns without complex calculations."""
        self.variety_window.append(variety)
        if len(self.variety_window) < self.window_size:
            return None
            
        # simple convergence check
        latest_values = [sum([v.dispersal, v.intensity, v.complexity])/3 
                        for v in self.variety_window]
        if all(abs(latest_values[i] - latest_values[i-1]) < 0.1 
               for i in range(1, len(latest_values))):
            return "settling"
        return None

class QueryHomeostat:
    """A homeostat for maintaining conditions conducive to query formation."""
    
    def __init__(self):
        self.environment = Environment(
            state=SystemState.SETTLING,
            variety=Variety(),
            last_response="",
            history=deque(maxlen=5), # keeping only recent history
            momentum = 0.0,
            persistence = 0
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

        # merging elictation prompts from depricated VarietyRegulatory class
        # currently a bit naff
        # [!] read up on ELIZA and hone these as appropriate
        self.expansion_prompts = [
            "What else is present?",
            "Where else does your attention move?",
            "What other aspects feel alive?",
            "What remains unspoken?",
            "What other threads emerge?"
        ]

        self.emergence_prompts = [
            "What question begins begin to form?",
            "How might this question want to be asked?",
            "What shape does this query take?",
            "How does this question hold your situation?",  # quite like this one
            "What query emerges from this exploration?"
        ]

        self.hot_markers = {
            'exclamations': r'!+|\?!',
            'all_caps': r'\b[A-Z]{2,}\b',  # captures any word of 2+ capital letters
            'intensifiers': r'\b(very|really|absolutely|completely|totally)\b',
            'emphasis': r'\*\*|__|!!+|\?{2,}',
            'urgency': r'\b(now|immediately|suddenly|always|never|must|need)\b'
        }

        self.cool_markers = {
            'qualification': r'\b(perhaps|maybe|might|could|somewhat|sometimes|slowly)\b',
            'distance': r'\b(observe|notice|sense|reflect)\b',
            'modulation': r'[;:]|\.{2,}|—'
        }

    def validate_input(self, input_text: str) -> bool:
        """Validate input before processing."""
        if not input_text or not isinstance(input_text, str):
            raise ValueError("Invalid input: must be non-empty string")
        if len(input_text) > 1000:  # Add reasonable limits
            raise ValueError("Input exceeds maximum length")
        return True

    def apply_depth(self, text: str) -> str:
        """Apply spatial/depth pattern to response."""
        return self.depth_patterns[self.environment.depth_level - 1].format(text)

    def _get_state_response(self, input_text: str, state: SystemState) -> str:
        """State response generation."""
        response_map = {
            SystemState.SETTLING: lambda: self.settling_response(),
            SystemState.EXPANDING: lambda: self.expanding_response(),
            SystemState.CONTAINING: lambda: self.containing_response(input_text),
            SystemState.DWELLING: lambda: self.dwelling_response(input_text),
            SystemState.EMERGING: lambda: self.emerging_response()
        }
        return response_map.get(state, lambda: self.settling_response())()

    def containing_response(self, input_text: str) -> str:
        """Generate containing response for high variety."""
        words = input_text.split()
        key_phrase = " ".join(words[:5]) + "..." if len(words) > 5 else input_text
        response = self.containing_patterns[self.environment.depth_level - 1].format(key_phrase)
        return self.apply_timing(response)

    def expanding_response(self) -> str:
        """Generate response to encourage expansion."""
        return self.apply_timing(
            self.expansion_prompts[self.environment.depth_level - 1]
        )

    def dwelling_response(self, input_text: str) -> str:
        """Generate response for dwelling with content."""
        words = input_text.split()
        if words:
            focus_word = words[len(words)//2]
            return self.apply_timing(self.apply_depth(f"staying with: {focus_word}"))
        return self.apply_timing("staying with what's present")

    def emerging_response(self) -> str:
        """Generate response for query emergence."""
        return self.apply_timing(
            self.emergence_prompts[self.environment.depth_level - 1]
        )

    def settling_response(self) -> str:
        """Generate initial settling response."""
        return self.apply_timing("Take a moment to settle into this space")
    
    def apply_timing(self, text: str) -> str:
        """Apply timing pattern to response."""
        return f"{text}\n{self.pause_patterns[self.environment.pause_level - 1]}"

    def generate_response(self, input_text: str) -> str:
        """Generate response based on input and current environment."""
        try:
            # validate input and ass variety
            self.validate_input(input_text)
            variety = self.assess_variety(input_text)

            # explicitly update environment's variety
            self.environment.variety = variety

            # regulate variety
            new_state = self.regulate_variety(variety)

            # update environment
            self.environment.update(variety, new_state)

            # generate state-specific response
            response = self._get_state_response(input_text, new_state)
            self.environment.last_response = response
            return response

        except Exception as e:
            raise HomeostatError(f"Response generation failed: {str(e)}")

    def assess_variety(self, input_text: str) -> Variety:
        """Assess the variety of user input and return a populated Variety object."""

        # dispersal: analyse rhythmic patterns and pacing
        dispersal = self._assess_dispersal(input_text)

        # intensity: sense the "temperature" and emotional tone
        intensity = self._assess_intensity(input_text)
        
        # complexity: detect conceptual density and interrelatedness
        complexity = self._assess_complexity(input_text)
        
        return Variety(dispersal, intensity, complexity)
    
    def _assess_dispersal(self, text: str) -> float:
        """Analyse rhythms and pacing to assess dispersal."""
        # core focus: rythmic scattering
        # how attention and expression are spread across the interaction space
        # more about pattern than content; fluctuations in the flow of language
        # not "messiness"; structural rhythm and its interruptions
        # irregular patterns indicate scattered attention or thought processes

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

        # combined weighting prioritising rhythm and flow; return a normalised dispersal value between 0 and 1
        dispersal = (
            0.5 * metrics['rhythmic_scatter'] +     # primary rhythm measure
            0.3 * disruption_markers +              # secondary flow measure
            0.2 * breaks                            # tertiary structure measure
        )
    
        return min(max(dispersal * 2.0, 0.0), 1.0)

    def _detect_intensity_shift(self, sent1: str, sent2: str) -> bool:
        """Detect significant shifts in intensity between sentences."""
        # a function for intensity assessment
        # [?] are 'hot_markers' and 'cool_markers' undefined attributes?
        def get_intensity_markers(text:str) -> dict:
            return {
                'hot': sum(1 for pattern in self.hot_markers.values() 
                          if re.search(pattern, text.lower())),
                'cool': sum(1 for pattern in self.cool_markers.values() 
                          if re.search(pattern, text.lower()))
            }
        
        m1 = get_intensity_markers(sent1)
        m2 = get_intensity_markers(sent2)

        # compare intensity profiles
        return abs((m1['hot'] - m1['cool']) - 
                    (m2['hot'] - m2['cool'])) > 1

    def _assess_intensity(self, text: str) -> float:
        """Sense the "temperature" and emotional tone to assess intensity."""
        # core focus: energetic "charge", embodied experience
        # the force or pressure behind expression
        # shifts in emotion, tone, or energy
        # from tightly wound containment to explosive release

        if not text.strip():
            return 0.0

        metrics = {}
        text_len = max(len(text.split()), 1) # avoid division by zero

        # calculate hot markers count, with higher weighting
        hot_count = sum(len(re.findall(pattern, text.lower())) * 2
                        for pattern in self.hot_markers.values())

        # calculate cool markers count
        cool_count = sum(len(re.findall(pattern, text.lower()))
                         for pattern in self.cool_markers.values())
        
        # convert counts to normalised intensity score
        metrics['pressure'] = float(hot_count + cool_count) / text_len

        # 1. embodied references
        embodied_patterns = {
            'somatic': r'\b(feel|felt|body|heart|breath|hands|chest|stomach|gut|throat)\b',
            'personal': r'\b(I|me|my|mine)\b',
            'experiential': r'\b(sense|experience|perceive|aware)\b'
        }
        metrics['embodied'] = sum(
            len(re.findall(pattern, text.lower()))
            for pattern in embodied_patterns.values()
        ) / text_len

        # 2. repetition patterns
        words = text.lower().split()
        repetitions = len([w for i, w in enumerate(words) 
                          if i > 0 and w == words[i-1]])
        metrics['repetition'] = repetitions / text_len

        # 3. cross-sentence intensity shifts
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if len(sentences) > 1:
            shift_intensity = sum(1 for i in range(len(sentences)-1)
                                  if self._detect_intensity_shift(sentences[i],
                                                                  sentences[i+1]))
            metrics['shifts'] = shift_intensity / (len(sentences) - 1)
        else:
            metrics['shifts'] = 0.0

        # combined weighting; return a normalised intensity value between 0 and 1
        intensity = (
            0.40 * metrics['pressure'] +    # primary structural tension
            0.25 * metrics['embodied'] +    # somatic anchoring
            0.20 * metrics['shifts'] +      # temporal dynamics
            0.15 * metrics['repetition']    # pattern emphasis
        )

        return min(max(intensity * 2.5, 0.0), 1.0)

    def _assess_complexity(self, text: str) -> float:
        """Gague conceptual density and interrelatedness to assess complexity."""
        # core focus: conceptual density, cognitive mapping
        # how ideas nest and relate to each other
        # revealed through patterns of conceptual and temporal connection
        
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
        movement_patterns = {
            'scale': len(re.findall(r'\b(part|whole|specific|general)\b', text.lower())),
            'time': len(re.findall(r'\b(now|then|before|after|while|during)\b', text.lower())),
            'space': len(re.findall(r'\b(here|there|between|across)\b', text.lower()))
        }

        movement_score = sum(movement_patterns.values())

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
            'nested': len(re.findall(r'\b(within|inside|containing|embedded)\b', text.lower())),
            'recurring': len(re.findall(r'\b(again|back|return|cycle|recur|echo)\b', text.lower()))
        }

        try:
            # combined weighting; return a normalised complexity value between 0 and 1
            complexity = (
                0.30 * metrics['connections'] +                         # primary relational structure
                0.25 * sum(metrics['shifts'].values()) / text_len +     # perspective shifts
                0.25 * metrics['abstraction'] +                         # abstractions and concepts
                0.10 * movement_score +                                 # conceptual movement across scales
                0.10 * sum(metrics['recursion'].values()) / text_len    # self-reference
            )

            return min(max(complexity * 2.5, 0.0), 1.0)
        except Exception as e:
            raise VarietyAssessmentError(f"Error calculating complexity: {str(e)}")

    def regulate_variety(self, variety: Variety) -> SystemState:
        """Determine appropriate system state based on variety measures."""
        # calculate overall variety level
        total_variety = (variety.dispersal + variety.intensity + variety.complexity) / 3.0
        momentum = self.environment.momentum
    
        # minimal state tracking
        # will update environment history if needed
        # this version maintains a small history buffer while 
        # keeping the core logic simple and deterministic
        # [!] TODO look at this and work it through; can we swap this out for a deque?
        if hasattr(self.environment, 'history'):
            self.environment.history.append(variety)    # store variety object
            if len(self.environment.history) > 5:
                self.environment.history.popleft()      # [?] using popleft() for deque; WHY?

        # simple state transition rules based on dominant variety measure
        # this can get more subtle later, if helpful, but at the cost of smallness
        if total_variety > 0.8:
            return SystemState.CONTAINING
        elif variety.dispersal > 0.7:
            return SystemState.DWELLING
        elif variety.complexity > 0.7:
            return SystemState.CONTAINING
        elif self.environment.persistence > 3 and momentum < 0.1:
            return SystemState.EXPANDING
        elif variety.complexity < 0.2:
            return SystemState.SETTLING
        else:
            return SystemState.EMERGING

    def _get_state_response(self, input_text: str, state: SystemState) -> str:
        """Map system states to response patterns."""
        response_map = {
            SystemState.SETTLING: lambda: self.settling_response(),
            SystemState.EXPANDING: lambda: self.apply_timing("What else is present?"),
            SystemState.CONTAINING: lambda: self.apply_timing(
                self.containing_patterns[self.environment.depth_level -1].format(
                    " ".join(input_text.split()[:5]) + "..."
                )
            ),
            SystemState.DWELLING: lambda: self.apply_timing("staying with what's present"),
            SystemState.EMERGING: lambda: self.apply_timing("What question begins to form?")
        }
        return response_map.get(state, lambda: self.settling_response())()

class CLISession:
    def __init__(self, homeostat: QueryHomeostat):
        self.homeostat = homeostat
        self.rhythm = DialogueRhythm()
        self.state = SessionState.ACTIVE
        self._last_input_time: Optional[float] = None

class HomeostatError(Exception):
    """Base exception for all homeostat errors."""
    def __init__(self, message: str, context: Dict = None):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = time.time()

class InputValidationError(HomeostatError):
    """Invalid input error."""
    pass

class VarietyAssessmentError(HomeostatError):
    """Error in variety assessment"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}

class StateTransitionError(HomeostatError):
    """Invalid state transition error."""
    pass

def demonstrate_usage():
    """Simulate a sequence of interactions to showcase state progression."""
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
    print("System: " + homeostat.settling_response())
    time.sleep(2)  # simulate a pause

    # process each input to see how the state evolves
    for i, user_input in enumerate(inputs):
        print(f"\nUser: {user_input}")

        # generate response based on user input and current system state
        response = homeostat.generate_response(user_input)

        # print system's response and display current variety and state
        print(f"System: {response}")
        print(f"Variety - DISP. {homeostat.environment.variety.dispersal:.2f}, "
              f"INT. {homeostat.environment.variety.intensity:.2f}, "
              f"COMP. {homeostat.environment.variety.complexity:.2f}")
        print(f"State: {homeostat.environment.state.name}")
        
        # small simulated delay
        time.sleep(2.5)

if __name__ == "__main__":
    demonstrate_usage()