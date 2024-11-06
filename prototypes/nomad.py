import typer
import time
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Set, Any
from enum import Enum

class Command(str, Enum):
    traverse = "traverse"
    observe = "observe"
    exit = "exit"

class ObjectCategory(str, Enum):
    PERSONAL = "personal"           # objects with personal significance
    EPHEMERAL = "ephemeral"         # temporary or changing elements
    PERSISTENT = "persistent"       # stable environmental features

class TimePhase(Enum):
    DAWN = "dawn"
    DAY = "day"
    DUSK = "dusk"
    NIGHT = "night"

def main():
    cathedral = NomadCathedral()
    typer.echo("The space forms around you, borrowing from your surroundings...")
    typer.echo(cathedral.establish_presence())

    while True:
        try:
            command = typer.prompt(
                "What would you like to do?",
                type=Command
            )

            if command == Command.exit:
                typer.echo("The cathedral melts back into potential...")
                break

            commands = {
                Command.traverse: lambda: cathedral.space.traverse(
                    typer.prompt("Where would you like to go?", type=str)
                ),
                Command.observe: cathedral.borrow_scenery
            }

            result = commands[command]()
            typer.echo(result)

        except Exception as e:
            typer.echo(f"Error: {e}")

@dataclass
class BorrowedScenery:
    celestial: str
    proximate: str
    ambient: str
    timestamp: datetime = field(default_factory=datetime.now)

class Context:
    """The querent's immediate situation and temporal state"""
    def __init__(self):
        self.immediate_situation = {
            'time': None,
            'season': None,
            'location': None,
            'atmosphere': None,
            'current_activity': None,
            'emotional_state': None
        }

class ThresholdState(Enum):
# need to reflect on and explore the implied ontology, here
    DORMANT = "dormant"         # inactive but present (might be better as 'latent'?)
    EMERGING = "emerging"       # beginning to manifest
    ACTIVE = "active"           # fully present
    FADING = "fading"           # diminishing but still navigable
    SEALED = "sealed"           # temporarily uncrossable

class ThresholdType(Enum):
# [?] should this be limited to spatio-temporal thresholds, or more general-purpose?
    SPATIAL = "spatial"         # between physical/conceptual locations
    TEMPORAL = "temporal"       # between times/durations
    MATERIAL = "material"       # between forms/substances
    PERCEPTUAL = "perceptual"   # between ways of seeing/experiencing

@dataclass
class Threshold:
    """A point of resistance, transition, or transformation"""
    name: str
    connecting: tuple[str, str]                         # explicit connection between two anchors; ensure anchors are correctly referenced
    conditions: Dict[str, float]                        # circumstances affecting passage
    qualities: Set[str]                                 # characteristic attributes
    # current state
    intensity: float = 0.0                              # resistance/significance of crossing
    state: ThresholdState = ThresholdState.DORMANT      # dynamic accessibility
    last_crossed: Optional[datetime] = None
    crossing_history: List[Dict] = field(default_factory=list)

    def evaluate_crossing(self):
        """Determine if and how crossing occurs"""
        # placeholder evaluation logic
        return True
    
    def record_crossing(self, context: Context):
        """Record crossing attempt and outcome"""
        self.crossing_history.append({
            'timestamp': datetime.now(),
            'context': context.snapshot(),
            'intensity': self.intensity
        })
        self._update_intensity(context)

class PartState(Enum):
    AVAILABLE = 'available'                     # in stock, ready for use
    CONFIGURED = 'configured'                   # currently deployed in a cathedral configuration
    RESTING = 'resting'                         # temporarily unavailable
    TRANSITIONING = 'transitioning'             # between states (not clear what this means in practice)

@dataclass(frozen=True)
# make immutable for hashability
class Part:
    id: str
    nature: tuple[str, ...]                     # material, conceptual, hybrid, basically anything
    state: PartState = PartState.AVAILABLE      # a default value
    ephemerality: float = 0.0                   # 0.0 = ephemeral, 1.0 = obdurate
    permanence: bool = False                    # actual permanence should be a Bool, so key items don't get composted

    configurations: List[Dict] = field(default_factory=list)
    last_used: Optional[datetime] = None
    rest_period: Optional[timedelta] = None

    def calculate_rest_period(self) -> timedelta:
    # [?] what factors influence rest?
    # [?] how do temporal factors influence part availability
        pass

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if not isinstance(other, Part):
            return NotImplemented
        return self.id == other.id

@dataclass
class PartIdentity:
    id: str
    relations: Dict[str, float] = field(default_factory=dict)
    history: List[Dict] = field(default_factory=list)
    
    def evolve(self, interaction: Dict):
        """Identity emerges through history"""
        self.history.append(interaction)
        self._update_relations(interaction)
        return self._calculate_current_identity()
    
class PartNetwork:
    """Distributed state management across autonomous parts"""
    # [?] how autonomous are they, exactly?
    def __init__(self):
        self.parts: Dict[str, Part] = {}
        self.interactions: List[Dict] = []
    
    def register_interaction(self, parts: Set[str], context: Context):
        """Record interaction between parts"""
        for part_id in parts:
            self.parts[part_id].process_interaction(context)
            self._update_network_relations(part_id, parts - {part_id})

@dataclass
class Configuration:
    """Dynamic configuration that evolves with context"""
    parts: Set[str]
    timestamp: datetime
    context: Dict[str, Any]
    thresholds: List[Threshold]
    
    def adapt(self, new_context: Context):
        """Allow configuration to develop"""
        self.context_history.append(new_context)
        self._adjust_relations()
        self._reconsider_parts()

    def dissolve(self):
        """Return parts to stock with updated histories"""
        for part in self.parts:
            part.configurations.append({
                'timestamp': self.timestamp,
                'context': self.context,
                'duration': datetime.now() - self.timestamp
            })
            part.state = PartState.RESTING
            part.rest_period = self._calculate_rest_period(part)

class Stock:
# [!] need to write a proper part selection algorithm
    def __init__(self):
        self.parts: Dict[str, Part] = {}

    def add_part(self, part: Part):
        """Add a new part to stock"""
        self.parts[part.id] = part
    
    def select_parts(self, context: Context) -> List[Part]:
        """Select parts for a new configuration"""
        available = [p for p in self.parts.values() 
                    if p.state == PartState.AVAILABLE]
        # consider: context alignment, historical patterns, rest periods
        return self._filter_and_rank(available, context)

    def _filter_and_rank(self, parts: List[Part], context: Context) -> List[Part]:
        return sorted(parts, key=lambda p: self._calculate_fitness(p, context), reverse=True)
        # no idea what this second bit is doingggggg

    def _calculate_fitness(self, part: Part, context: Dict[str, Any]) -> float:
        # placeholder fitness calculation
        return 1.0

@dataclass
class CathedralState:
# [?] what persists between sessions, and what resets?
    configuration: Configuration
    temporal_phase: TimePhase
    borrowed_elements: Dict[str, Any]
    thresholds: List[Threshold]

class PartsCatalogue:               # laminated book of dreams; if this is the metaphor, what else does it suggest?
    def __init__(self):
        self.parts: Dict[str, Part] = {}
        self.usage_patterns: Dict[str, List[str]] = {}

    def suggest_constellation(self) -> List[Part]:
        """Propose parts that resonate with current context"""

class ConfigurationCycle:
    def establish(self):
        """Initial cathedral manifestation"""
        parts = self.parts_catalogue.suggest_constellation(self.context)
        configuration = self.assemble_configuration(parts)
        self.manifest_thresholds(configuration)

    def reconfigure(self, trigger: str):
        """Respond to significant changes"""
        if self.should_reconfigure(trigger):
            self.dissolve_current()
            self.establish()

    def dissolve_current(self):     # 'dissolve' is a tad strong
        """Return parts to inventory with updated histories"""
        for part_id in self.current_configuration.active_parts:
            part = self.stock.parts.get(part_id)
            if part:
                part.configurations.append({
                    'timestamp': self.current_configuration.timestamp,
                    'context': self.current_configuration.context,
                    'duration': datetime.now() - self.current_configuration.timestamp
                })
                part.state = PartState.RESTING
                part.rest_period = self.calculate_rest_period()

class Environment:
    """The Nomad Cathedral's current manifestation"""
    def __init__(self):
        self.cathedral_state = {
            'configuration': None,
            'borrowed_elements': {},
            'active_elements': set()
        }
        # [?] might be too rigid for representing a dynamic, evolving structure?
        self.atmospheric_conditions = {
            'light_quality': None,
            'ambient_sounds': [],
            'perceived_temperature': None
        }
    
    def integrate_elements(self, borrowed):             # [?] what is borrowed? a dict, a class, what fields?
        self.atmospheric_conditions.update(borrowed)    # [?] what's valid to update?
        self.adjust_configuration()                     # [?] what configurations are possible?
        self.update_ephemera()                          # [?] What constitutes ephemera?

@dataclass
class Anchor:
    """A fixed point"""
    connections: List[str]
    description: str
    permanent: bool = True

class Space:
    """The Nomad Cathedral's dynamic spatiality"""
    def __init__(self):
        self.anchors: Dict[str, Anchor] = {
            "hearth": Anchor(
                connections=["sky_window"],
                description="A central space for contemplation and interpretation"
                ),
            "sky_window": Anchor(
                connections=["hearth"],
                description="An opening to observe the sky and weather"
                )
            }
        self.thresholds: Dict[str, Threshold] = {}      # points of transition/intensity
        self.ephemera: List[Dict[str, Any]] = []        # a more fluid, dynamic layer of "stuff"
        self.current_focus: Optional[str] = "hearth"    # current point of attention
        self.previous_focus: Optional[str] = None       # for tracking transitions

    def sense_space(self) -> Dict[str,Any]:
        """Return current spatial configuration and awareness"""
        return {
            "focus": self.current_focus,
            "anchors": self._gather_nearby_anchors(),
            "thresholds": self._find_active_thresholds(),
            "ephemera": self._collect_present_ephemera()
        }
    
    def _find_active_thresholds(self) -> List[Threshold]:
        """Identify currently active thresholds"""
        active_thresholds = []

        # consider transitions between anchors
        if self.previous_focus and self.current_focus:
            active_thresholds.append(
                Threshold(
                    name=f"{self.previous_focus}_to_{self.current_focus}",
                    intensity=0.6,
                    qualities=["transitional"],
                    anchors={self.previous_focus, self.current_focus}
                )
            )

        # consider temporal thresholds
        current_time = datetime.now()
        if 5 <= current_time.hour <= 7:
            active_thresholds.append(
                Threshold(
                    name="dawn_threshold",
                    intensity=0.7,
                    qualities=["temporal", "luminous"],
                    anchors={"sky_window"}
                )
            )
            
        return active_thresholds

    def traverse(self, direction: str) -> str:
        if direction in self.anchors[self.current_focus].connections:
            self.previous_focus = self.current_focus
            self.current_focus = direction
            return self.anchors[direction].description
        return f"Cannot move to {direction} from here."

    def _describe_current_focus(self) -> str:
        descriptions = {
            "hearth": "You stand in the central hearth.",               # better description needed
            "sky_window": "Light pools around you in the sky window."   # better description needed
        }
        return descriptions.get(self.current_focus, "You are somewhere undefined.")

    def _calculate_resonance(self, threshold: Threshold) -> float:
        """Calculate current resonance with threshold"""
        # consider: current context, recent movements, environmental conditions, temporal phase
        pass

    def update_context(self, borrowed_scenery: BorrowedScenery):
        """Integrate environmental awareness"""
        self._adjust_threshold_intensities(borrowed_scenery)
        self._update_ephemera()
        self._recalculate_focus()

    def integrate_environment(self, borrowed: BorrowedScenery):
        self.ephemera = self._derive_ephemera(borrowed)
        self.thresholds = self._adjust_thresholds(borrowed)
        return self._generate_atmosphere()

@dataclass
class NavigationContext:
    temporal_phase: str
    environmental_conditions: Dict[str, Any]
    recent_crossings: List[str] = field(default_factory=list)

@dataclass
class Constellation:
# [?] maybe better to name this 'assemblage'? or something else entirely?
    """A specific arrangement of parts in space and time"""
    elements: Set[str]
    anchors: Dict[str, "Anchor"]
    thresholds: List["Threshold"]
    temporal_context: datetime

    def _generate_context(self) -> Dict[str, Any]:
        return {
            'timestamp': self.temporal_context,
            'elements': list(self.elements),
            'anchors': list(self.anchors.keys()),
            'thresholds': [t.name for t in self.thresholds]
        }

    def arrange(self) -> Configuration:
        """Transform constellation into concrete configuration"""
        return Configuration(
            parts=set(self.elements),
            timestamp=self.temporal_context,
            context=self._generate_context(),
            thresholds=self.thresholds
        )

class TemporalContext:
    natural_time: datetime
    ritual_time: int            # session progression
    memory_time: List[Dict]     # past configurations

class TemporalFlow:
# [?] maybe better to name this 'duration'? or something else entirely?
    def __init__(self):
        # natural time
        self.clock_time: datetime = datetime.now()
        self.day_phase: str = self._calculate_day_phase()
        self.season: str = self._calculate_season()
        # ritual/interaction time
        self.session_start: datetime = datetime.now()
        self.interaction_count: int = 0
        self.session_phase: str = "beginning"
        # memory
        self.configuration_history: List[Dict] = []
        self.session_count: int = 0

@dataclass
class GatheredObject:
    name: str
    category: ObjectCategory
    description: str
    significance: str
    first_noticed: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    associations: List[str] = field(default_factory=list)
    qualities: Dict[str, float] = field(default_factory=dict)

    def update_presence(self, description: Optional[str] = None):
        """Record that object was seen again, with optional description updates"""
        self.last_seen = datetime.now()
        if description:
            self.description = description

class ObjectGathering:
    """Structured gathering of objects from the user's environment"""
    
    def __init__(self):
        self.gathered_objects: Dict[str, GatheredObject] = {}
        self.gathering_prompts = {
            ObjectCategory.PERSONAL: [
                "What object near you holds meaning?",
                "What's something you keep close?",
                "Which object here has a story?"
            ],
            ObjectCategory.EPHEMERAL: [
                "What's temporary or fleeting?",
                "What might be different tomorrow?",
                "What traces of activity do you notice?"
            ],
            ObjectCategory.PERSISTENT: [
                "What's always present in this space?",
                "What forms the backbone of this environment?",
                "What here remains constant?"
            ]
        }

    def gather_objects(self, typer) -> List[GatheredObject]:
        """Main gathering loop with structured prompts"""
        typer.echo("\nLet's gather some objects from your environment...")
        gathered = []

        # gather one object from each category
        for category in ObjectCategory:
            typer.echo(f"\n{self._get_category_description(category)}:")
            prompts = self.gathering_prompts[category]

            # get random prompt for variety
            prompt = random.choice(prompts)

            # gather object details
            name = typer.prompt(prompt)
            if name.lower() == 'skip':
                continue
                
            description = typer.prompt(
                "Describe it",
                default="It has presence"
            )

            significance = typer.prompt(
                "What makes it significant here?",
                default="It belongs"
            )

            # Create and store object
            obj = GatheredObject(
                name=name,
                category=category,
                description=description,
                significance=significance
            )

            self.gathered_objects[name] = obj
            gathered.append(obj)
            
            # Brief pause
            time.sleep(0.5)

        return gathered

    def _get_category_description(self, category: ObjectCategory) -> str:
        """Get human-readable category descriptions"""
        descriptions = {
            ObjectCategory.PERSONAL: "Personal objects",
            ObjectCategory.EPHEMERAL: "Temporary features",
            ObjectCategory.PERSISTENT: "Permanent elements"
        }
        return descriptions[category]

    def integrate_objects(self, space: Space, objects: List[GatheredObject]):
        """Integrate gathered objects into the cathedral space"""
        for obj in objects:
            # create ephemeral elements for (from?) ephemeral objects
            if obj.category in [ObjectCategory.EPHEMERAL]:
                space.ephemera.append({
                    "type": "gathered_object",
                    "name": obj.name,
                    "description": obj.description,
                    "created_at": datetime.now(), 
                    "duration": 3600
                })
            # create more persistent elements for personal and persistent objects
            elif obj.category in [ObjectCategory.PERSONAL, ObjectCategory.PERSISTENT]:
                # create a new part from the object
                part = Part(
                    id=f"gathered_{obj.name.lower().replace(' ', '_')}",
                    nature=["physical", "gathered"],
                    state=PartState.AVAILABLE,
                    ephemerality=0.3 if obj.category == ObjectCategory.PERSONAL else 0.1
                )
                # add to stock
                space.stock.add_part(part)

class NomadCathedral:
    def __init__(self):
        self.stock = Stock()
        self.space = Space()
        self.borrowed_scenery: Optional[BorrowedScenery] = None
        self.configured_parts: Set[str] = set()
        self.current_phase = TimePhase.DAWN

    def establish_presence(self):
        """Initial sessional assembly, configuring cathedral from stock"""
        try:
            available_stock = self.retrieve_stock()
            if not available_stock:
                # initialise with default parts if stock is empty
                self._initialise_default_stock()
                available_stock = self.retrieve_stock()
            self.borrowed_scenery = self.borrow_scenery()
            configuration = self.configure_apparatus(available_stock, set())
            self.establish_thresholds(configuration)
            return "The cathedral manifests around you..."
        except Exception as e:
            return f"The cathedral struggles to form: {str(e)}"

    def _initialise_default_stock(self):
        """Initialise stock with some default parts"""
        default_parts = [
            Part(
                id="minster_stone",
                nature=["physical", "anchoring"],
                state=PartState.AVAILABLE,
            ),
            Part(
                id="mediterranean_light",
                nature=["atmospheric", "temporal"],
                state=PartState.AVAILABLE,
            ),
            Part(
                id="evening_bells",
                nature=["sonic", "temporal"],
                state=PartState.AVAILABLE
            )
        ]
        for part in default_parts:
            self.stock.add_part(part)

    def retrieve_stock(self) -> Set[str]:
        return {part_id for part_id, part in self.stock.parts.items() if part.state == "available"}

    def configure_apparatus(self, stock: Set[str], borrowed: Set[str]) -> Configuration:
        """Assemble cathedral from available parts"""
        parts = self.select_elements(stock, borrowed)
        constellation = self._form_constellation({part.id for part in parts})
        return constellation.arrange()
    
    def select_elements(self, stock: Set[str], borrowed: Set[str]) -> Set['Part']:
        """Select elements for cathedral configuration based on stock and borrowed scenery"""
        selected = set()
        # add core elements from stock
        for part_id in stock:
            part = self.stock.parts.get(part_id)
            if part and self._is_compatible(part, borrowed):
                selected.add(part)
        # integrate borrowed elements
        for part_id in borrowed:
            part = self.stock.parts.get(part_id)
            if part and len(selected) < 7:  # arbitrary limit for "smallness" (yessssssss)
                selected.add(part)
        return selected
    
    def _is_compatible(self, part: Part, borrowed: Set[str]) -> bool:
        """Check if a stock element is compatible with borrowed scenery"""
        # implementation could consider: part nature, current configuration, context
        return True

    def borrow_scenery(self) -> str:
        # current implementation is linear and a bit rigid
        # think about: cyclic observation patterns, layered sensory prompts, memory of previous borrowings
        # need to better embodying the sense of Shakkei, OF "CAPTURING LANDSCAPE ALIVE"
        """Gather environmental context through user interaction"""
        typer.echo("Take a moment to observe your environment...")
        time.sleep(2)

        celestial = typer.prompt(
            "Through gaps in the ceiling, you glimpse...",
            default="a vast expanse"
            )

        typer.echo(typer.style("Let your gaze wander...", dim=True))
        time.sleep(1)

        proximate = typer.prompt(
            "What draws your attention?",
            default="shadows and light"
        )

        typer.echo(typer.style("What is present?", dim=True))
        time.sleep(1)
        
        ambient = typer.prompt(
            "The air carries...",
            default="a whisper of distant movement"
        )

        self.borrowed_scenery = BorrowedScenery(
            celestial=celestial,
            proximate=proximate,
            ambient=ambient
        )

        # reflect back the integration
        return f"The cathedral resonates with {celestial}, while {proximate} shapes its forms. {ambient} moves through its spaces."

    def _form_constellation(self, elements: Set[str]) -> Constellation:
        """Form a potential arrangement of elements"""
        space_thresholds = self.space._find_active_thresholds()
        stock_thresholds = self.stock._identify_part_thresholds(elements)

        return Constellation(
            elements=elements,
            anchors=self.space.anchors,
            thresholds=space_thresholds + stock_thresholds,
            temporal_context=datetime.now()
        )

    def establish_thresholds(self, configuration: Configuration) -> None:
        """Establish active thresholds based on configuration and context"""
        spatial_thresholds = self.space._find_active_thresholds()
        configuration_thresholds = self._derive_configuration_thresholds(configuration)
        self.active_thresholds = spatial_thresholds + configuration_thresholds

    def _derive_configuration_thresholds(self, configuration: Configuration) -> List[Threshold]:
        """Generate thresholds from current configuration"""
        thresholds = []
        for part_id in configuration.parts:
            part = self.stock.parts.get(part_id)
            if part and any(nature in part.nature for nature in ["transitional", "liminal"]):
                thresholds.append(self._create_part_threshold(part))
        return thresholds
    
    def _create_part_threshold(self, part: Part) -> Threshold:
        return Threshold(name=f"{part.id}_threshold", connecting=(part.id, part.id), conditions={}, qualities=set())

if __name__ == "__main__":
    typer.run(main)