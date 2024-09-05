# Querent.py

## Unrefined Notes

- "situated software for tarot readers"; something we ourselves could use
- Bogostian carpentry to explore some of: combinatorics, "ostensive detachment" (Boyer), "black-boxing", intersubjective meaning-making
- positioning the tarot as a "jagged noetic substrate" (after Kyle Booten)
- computer-supported intuition/divination
- emphasising introspection over prediction
- a detournement or hijacking of generative language models and RAG systems (as "Generation-Augmented Retrieval")
- **brief:** creating a system that is not a static encoding of fixed meanings, but a tool for exploring associations and generative potential
- a conversational/dialogic elicitation system
- data persistence; building up some kind of a history/memory/residue/patina through sustained interaction; populating a knowledge base[^1]
- **constraint:** requires a physical deck to use (Tarot de Marseille?)

- how can we leverage the ELIZA effect to scaffold and encouraging elicitation, free association, etc.?

- seeking to support or sustain a spirit of open-ended exploration rather than arriving at definitive answers; aim is to facilitate discovery
- the program should engage in a collaborative, freeform dialogue, following the user's intuitive leaps, gently guiding but not constraining the direction of the conversation

- some kind of sense of accumulating readings over time (a log or journal of spreads, but also metrics about recurring cards, symbols, themes, motifs); as trace, patina, or residue?

- initially, a command line interface, with commands for
	- adding a new card interpretation
	- viewing existing interpretations
	- inputting a drawn spread
	- saving and loading interpretation data

- a data structure to store card interpretations; presumably a pre-populated dictionary, with the card names as keys and the interpretations as values
- functions for adding, viewing, and updating card interpretations
- when adding new interpretations, prompt the user for input and append it to the existing interpretation for that card, along with a timestamp; creating a record of how the user's understanding of each card evolves over time
- save the interpretation data to a file, and load it when the program starts, ensuring the user's personalised meanings persist across sessions

- with greater complexity, organise the program into classes and modules for better code structure and maintainability
	- e.g. Deck class to represent the tarot deck, Card class for individual cards, and a Reading class for inputting and storing readings

- thinking about "graceful degradation/failure"; how will the program handle errors or exceptions? (invalid inputs, missing files, etc.)

- how will the program handle user authentication and privacy? if the program is to be used by multiple users, it will be important to ensure each user's data is secure and private (does a Raspberry Pi deployment repattern this problem?)

- a graphical user interface using JSON Canvas, to make the program more visually appealing
	- particularly good for the spatial organisation of information
	- would integrate with Obsidian etc. (for importing/exporting, sharing, and annotating)
	- what limitations does this impose, in terms of compatible data formats?

- Provide an "explore" feature that generates dynamic spreads and interpretations based on the user's selection of key cards, attributes or themes. The algorithms enact Jodorowsky's methodology within Bogost's framework.

## Handling the dictionary or database?

- Some challenges in figuring out what interpretations to use as the common foundation or base ("factory settings"), prior to querent additions.

- ~~Relational Database Management System (RDBMS)?~~
- Document-Oriented Database? (e.g. MongoDB or CouchDB)
- Key-Value Store? (Redis or Riak)
- Graph Database? (Neo-four-J, or Amazon Neptune)
- Triplestore? (Apache Jena, RDF-four-J)

- Entity-attribute-value model? (EAV model; can add new attributes/values over time?)
	- entities: cards, suits, elements, other relevant concepts
	- attributes: properties, e.g. meaning, symbolism, imagery, astrological and numerological associations
	- values: specific interpretations?

## Entities and Attributes

1. **What are the core entities in the tarot domain? What key attributes describe each entity? Consider both standard meanings and personal interpretations.**
	- Cards (78 individual cards that make up a standard deck, each with its own unique imagery, symbolism, and meanings)
	- Suits (Minor Arcana divided into 4 suits: Wands (fire), Cups (water), Swords (air), and Pentacles/Coins (earth); each representing a different domain of life)
	- Arcana
		- Major Arcana: 22 cards numbered 0-21 that represent major life themes, karmic lessons, and archetypal energies; tell the story of "the Fool's journey"
		- Minor Arcana: 56 cards divided into 4 suits; reflect day-to-day issues, situational energies, personality traits, etc.
			- Court Cards: 16 court cards, divided between the 4 suits; can represent personality types or actual people
		- Readings: The art of selecting, laying out, and interpreting cards to gain insight into a situation of question; many different spreads exist [a reading is one instance of a spread?]
		- Querent: The person recieving the reading; their energy, starting query, and openness can influence the cards drawn, the reading, and the accumulation of interpretations

2. **How will you model the rich web of associations and correspondences between cards and other symbolic domains? (e.g. numerology, astrology, elements)**

	- **Entity-Attribute-Value (EAV) model**
		- *Entities*: Cards, Suits, Arcana, Spreads, Readings, Querents
		- *Attributes*: Meanings, imagery descriptions, positional meanings, combinations
		- *Values*: Specific interpretations,  associations, notes, personal reflections
	- [?] Does it make sense to think about the EAV model through a lens of "pace layers"?
	- Allows us to start with a base of standard interpretations, but easily extend it to accommodate querent-supplied notes and evolving personal understandings over time
	- Supports complex, many-to-many semantic relationships between cards and imagery in a schema-less way
	- Optimised for capturing sparse or ad-hoc properties in a space-efficient way
	- Means you can model things like:
		- Card A in Position X means Y
		- Card A followed by Card B suggests meaning Z
		- Cards X, Y, Z together indicate meaning Q
		- The figure in Card M is holding object O, which symbolises P
	- May require a more complex metadata schema to define entity types and valid attributes

	- Or: a **Graph Database**? (nodes and edges)

	- Or: a **Relational Model with Bridge Tables**? (sacrifices flexibility for more structure)

	- Maybe it's about **implementing an EAV model on top of a graph database** (e.g. Neo4j)
		- A good way to naturally represent the interconnected nature of tarot symbolism as a network of nodes (entities) and relationships
   		- Flexibly traverse and query this symbolic/interpretive graph to surface patterns and insights
   		- Leverage graph algorithms for recommendation, clustering, pathfinding etc to power generative, conversational interactions
   		- In conversation, use graph traversals to steer the dialogue and surface relevant symbolism and interpretations
   		- _Dynamically generate prompts, questions, and reflections based on the current state of the graph_
   		- Support an evolving, querent-specific "mental model" of the tarot based on interaction history
   		- Focusing your efforts on the fluid, conversational "hot path" will help create an engaging, responsive user experience
   		- Consider deploying Neo4j+Python on a Raspberry Pi for an optimised, offline-first "appliance"
  
  [!] We can start by programmatically inferring a base set of attributes from the JSON meanings, then provide an interface for users to add, edit, group and link attributes as they explore associations. The key is providing a flexible foundation that can evolve organically based on usage and insight.

## Relationships 

1. What are the key relationships between the entities? (e.g. Cards belong to Suits and Arcana)
2. How will you represent the sequence and positional meanings of cards in a Reading?
3. How will you associate Readings with Querents to build personal histories over time?

## Data Persistence and Portability

1. What file format will you use for local data storage to enable easy export/import? (e.g. JSON, SQLite)
2. How will you structure the data to be self-contained and avoid external dependencies for portability?
3. What privacy and security measures are needed to protect potentially sensitive personal reflections?

## Performance and Scalability 

1. What are the expected data volumes and read/write patterns based on intended usage?
2. Which operations need to be optimized for responsive, conversational interactions with querents?
3. Where might caching, indexing, or other optimizations be needed in the future as usage grows?

## Technology Choices

1. What are the pros/cons of relational (SQL) vs document (NoSQL) databases for this use case?
2. Which database options have the best documentation, community support, and Python integration?
3. How will you keep the stack simple, avoid vendor lock-in, and optimize for Raspberry Pi deployment?

## Import/Export and Interoperability

1. What data export formats will you support? (JSON, CSV, Markdown, etc)
2. How might you implement a git-like model for "forking" and "merging" interpretation databases? 
3. What kind of UI is needed for importing/exporting data and managing sharing with other querents?


## Stretch goals

- "an ontological map of the tarot"

- adding more generative language model functionalities, context-aware suggestions
	- how, specifically, will the program use generative language models or RAG systems?

- swappable dictionary/database files, to compare and contrast with other querents

- interoperability with some kind of journaling platform (outputting particular kinds of content as markdown files?)

- optimisation for Raspberry Pi deployment, as a dedicated portable device for tarot-based reflection

## Notes from Jorodowsky & Costa

- the tarot as a "projective instrument"?

- the program should go beyond just representing individual tarot cards; it needs data structures and logic to capture the full 78-card tarot deck as an interconnected system, or "mandala"; a "nomadic cathedral", in Jorodowsky's words, a portable device and system for sacred contemplation

- visualising the deck as an interconnected network that the user can explore?

- imagery and visual symbolism of the cards needs to be central, a core part of the interaction, rather than a library of predetermined, immutable keywords and fixed interpretations

- instead, it's about dwelling with (_within_?) the actual imagery, directing the querent's attention to specific symbols, colours, characters, etc., as prompts for the user's intuition?

- where there are characters or figures, have the program ask the querent to imagine themselves in the card imagery; forced first-perspective-taking

- need to put time and effort into _domain modelling_, deeply researching and mapping the ontology of our subject (the Tarot)

## Notes from Bogost: ontography, procedural rhetoric, and Bogostian carpentry

- what is the program's ontology and "umwelt" (surrounding world)? 

- its universe (initially) consists solely of the tarot system – the 78 cards, their meanings and associations, the rules for selecting and interpreting them; a highly constrained symbolic world, compared to the open-ended physical environments humans inhabit

- the data structure representing the tarot deck could be an "ontograph" - an exhaustive catalogue of the 78 cards and their myriad symbolic correspondences (numerological, elemental, astrological, etc.); this "raw data" would then be selectively sampled to generate readings?

- what is the lived temporality of the program? Humans contextualise the cards in terms of past, present and future; but the program exists in a kind of eternal present, instantly generating readings on demand; as it stands, it has no memory of previous readings nor anticipations of the future: each draw is a discrete event.

- the program's "body" is made up of code, data structures, and interface affordances. How does it sense and inhabit this digital embodiment? What are its means of interacting with and expressing itself in the world?

[^1]: Working on the assumption that this will require a database, structured in a way that supports retrieval?