import typer
from datetime import datetime, timedelta
from enum import Enum
import random
import math

app = typer.Typer()

# CYCLICALITY and RECURRENCE in temporal representation
# seeking ways to emphasise repetition and return;
# representing time as a continuous flow, a duration
# rather than discrete steps

class Season(Enum):
    SPRING = "Spring"
    SUMMER = "Summer"
    AUTUMN = "Autumn"
    WINTER = "Winter"

# the 'TreeRing' and 'TreeRingStructure' classes form
# the core of the temporal structure without
# specifying an interval or duration, and so
# support flexible, nested representations

class TreeRing:
    # tree ring metaphor
    # connotions: concentric/cyclical growth, (ac)cumulation, environmental record
    def __init__(self, start_date, end_date, data=None):
        self.start_date = start_date
        self.end_date = end_date
        self.data = data or [] # list of readings/interpretations

class TreeRingStructure:
    def __init__(self, start_date, end_date, zoom_level):
        self.ring_chars = ['(', '.', ')']  # Define ring_chars here
        self.start_date = start_date
        self.end_date = end_date
        self.zoom_level = zoom_level
        self.rings = self._generate_rings()
        self.current_position = 0 # position of the caret marker

    def navigate(self, direction):
        # rough prototype
        # implementing "intuitive" navigation in a circular or cyclic structure
        # may yet prove a nightmare
        if direction == 'left':
            self.current_position = max(0, self.current_position - 1)
        elif direction == 'right':
            self.current_position = min(len(self.rings) - 1, self.current_position + 1)

    def zoom(self, direction):
        if direction == 'in':
            self.zoom_level *= 2
        elif direction == 'out':
            self.zoom_level = max(1, self.zoom_level // 2)
        self.rings = self._generate_rings()
        self.current_position = min(self.current_position, len(self.rings) - 1)

    def _generate_rings(self):
        # generate rings based on zoom level
        # actual implementation will be much more complicated
        rings = []
        current_date = self.start_date
        while current_date < self.end_date:
            ring_end = min(current_date + timedelta(days=365 // self.zoom_level), self.end_date)
            rings.append(TreeRing(current_date, ring_end))
            current_date = ring_end
        return rings

    def visualise(self):
        total_width = 60 # adjust as required
        centre = total_width // 2

        # start with the innermost ring
        representation = ['(0)']

        # build rings outward
        for i in range(len(self.rings)):
            left_content = '.' * (i + 1)
            right_content = '.' * (i + 1)
            representation = ['('] + list(left_content) + representation + list(right_content) + [')']

        # pad to total width
        padding = (total_width - len(representation)) // 2
        final_representation = ' ' * padding + ''.join(representation) + ' ' * padding
    
        # add caret positional marker
        caret_position = padding + self.current_position + 1  # +1 for the opening '('
        caret_line = ' ' * caret_position + '^'
    
        return final_representation, caret_line

    def get_current_ring_info(self):
        ring = self.rings[self.current_position]
        return f"{ring.start_date.strftime('%Y-%m-%d')} to {ring.end_date.strftime('%Y-%m-%d')} ({len(ring.data)} readings)"

    def focus(self):
        ring = self.rings[self.current_position]
        return f"Focused on ring from {ring.start_date} to {ring.end_date}\nData: {ring.data}"
        # precise phrasing here may need some work

def get_season(date):
    # simplified season calculation
    # might need a smoother transition between seasons
    # and/or more responsive ways to handle seasonal difference
    # between physical locations
    month = date.month
    day = date.day
    if (month == 3 and day >= 20) or (month == 4) or (month == 5) or (month == 6 and day < 21):
        return Season.SPRING
    elif (month == 6 and day >= 21) or (month == 7) or (month == 8) or (month == 9 and day < 22):
        return Season.SUMMER
    elif (month == 9 and day >= 22) or (month == 10) or (month == 11) or (month == 12 and day < 21):
        return Season.AUTUMN
    else:
        return Season.WINTER

def generate_dummy_data(tree):
    for ring in tree.rings:
        num_readings = random.randint(0, 5)
        for _ in range(num_readings):
            reading_date = ring.start_date + timedelta(days=random.randint(0, (ring.end_date - ring.start_date).days))
            ring.data.append(f"Reading on {reading_date.strftime('%Y-%m-%d')}")

def display_interface(tree):
    current_date = datetime.now()
    typer.clear()
    typer.echo(f"Welcome to the wheel.")
    typer.echo(f"\nCurrent date: {current_date.strftime('%Y-%m-%d')}")
    typer.echo(f"Location: York, UK")
    # most immediately, designing for YORK and TARRAGONA (a Boolean? lol)
    # but need to replace this with a location field
    # and, further out, a more robust location system (lat+long?)
    # [?] are there geospatial libraries we could use?
    typer.echo(f"Current season: {get_season(current_date).value}")
    typer.echo(f"Zoom level: 1 year per {tree.zoom_level} rings") # this is clearly garbage
    # need to turn this "zoom level"/"view" into a better variable
    # [?] what other options are there?
    # full view, annual view, seasonal view, monthly view, custom view

    ring_representation, caret_line = tree.visualise()
    typer.echo(f"\n{ring_representation}")
    typer.echo(caret_line)

    typer.echo(f"{tree.get_current_ring_info()}\n")
    typer.echo("COMMANDS:")
    typer.echo("[z+] Zoom in        [z-] Zoom out")
    typer.echo("[<] Navigate left   [>] Navigate right")
    typer.echo("[f] Focus           [c] Cycle")
    typer.echo("[i] Input           [r] Retrieve")
    typer.echo("[q] Quit")
    # applying familiar command structures to new concepts
    # spatial metaphors here, ostensibly dealing with time & temporality
    # may need in-app help or orientation

def main_loop():
    start_date = datetime.now() - timedelta(days=365 * 5) # 5 years ago
    end_date = datetime.now()
    tree = TreeRingStructure(start_date, end_date, zoom_level=1)
    generate_dummy_data(tree)

    while True:
        display_interface(tree)
        command = typer.prompt("Enter command").lower()

        if command == 'z+':
            tree.zoom('in')
        elif command == 'z-':
            tree.zoom('out')
        elif command == '<':
            tree.navigate('left')
        elif command == '>':
            tree.navigate('right')
        elif command == 'f':
            typer.echo(tree.focus())
            typer.prompt("Press Enter to continue")
        elif command == 'q':
            break
        else:
            typer.echo("Invalid command")

@app.command()
def run():
    main_loop()

if __name__ == "__main__":
    app()