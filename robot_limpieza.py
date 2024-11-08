from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random


class RobotLimpieza(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        """Moves the agent to a random adjacent cell."""
        available_cells = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(available_cells)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        cell = next(
            (obj for obj in cell_contents if isinstance(obj, Cell)), None)
        if cell and cell.estado == 1:
            cell.estado = 0
        else:
            self.move()


class Cell(Agent):
    """Represents a cell in the grid that can be clean or dirty."""

    def __init__(self, unique_id, model, estado):
        super().__init__(unique_id, model)
        self.estado = estado


class RobotModel(Model):
    def __init__(self, num_agents, width, height, time_ejection, percentage_dirt):
        super().__init__()
        self.num_agents = num_agents
        self.time_ejection = time_ejection
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)

        total_cells = width * height
        num_dirty_cells = int(total_cells * percentage_dirt)

        self.initial_dirty_cells = num_dirty_cells  # Almacena las celdas sucias al inicio
        self.final_dirty_cells = num_dirty_cells    # Inicializa las celdas sucias al final

        dirty_positions = set()
        while len(dirty_positions) < num_dirty_cells:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            dirty_positions.add((x, y))

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                estado = 1 if (x, y) in dirty_positions else 0
                cell = Cell((x, y), self, estado)
                self.grid.place_agent(cell, (x, y))

        for i in range(self.num_agents):
            robot = RobotLimpieza(i, self)
            self.schedule.add(robot)
            x = 1
            y = 1
            self.grid.place_agent(robot, (x, y))

    def step(self):
        """Advance the model by one step."""

        if self.time_ejection <= 0:
            self.calculate_final_dirty_cells()  # Llama para calcular las celdas sucias al finalizar
            print(f"Initial dirty cells: {self.initial_dirty_cells}")
            print(f"Final dirty cells: {self.final_dirty_cells}")
            self.running = False
        else:
            self.schedule.step()
            self.time_ejection -= 1
            
    def calculate_final_dirty_cells(self):
        """Counts the remaining dirty cells at the end of the simulation."""
        self.final_dirty_cells = sum(
            1 for x in range(self.grid.width) for y in range(self.grid.height)
            if isinstance(self.grid.get_cell_list_contents((x, y))[0], Cell) and self.grid.get_cell_list_contents((x, y))[0].estado == 1
        )


def agent_portrayal(agent):
    if isinstance(agent, RobotLimpieza):
        portrayal = {
            "Shape": "circle",
            "Color": "blue",
            "Filled": True,
            "Layer": 1,
            "r": 0.5
        }
    elif isinstance(agent, Cell):
        color = "brown" if agent.estado == 1 else "white"
        portrayal = {
            "Shape": "rect",
            "Color": color,
            "Filled": True,
            "Layer": 0,
            "w": 1,
            "h": 1
        }
    return portrayal
