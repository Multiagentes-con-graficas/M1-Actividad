from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
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
        print("Moving to cell", new_position)

    def step(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        cell = next(
            (obj for obj in cell_contents if isinstance(obj, Cell)), None)
        if cell and cell.estado == 1:
            cell.estado = 0
            print("Cleaning cell")
        else:
            self.move()


class Cell(Agent):
    """Represents a cell in the grid that can be clean or dirty."""

    def __init__(self, unique_id, model, estado):
        super().__init__(unique_id, model)
        self.estado = estado


class RobotModel(Model):
    def __init__(self, num_agents, width, height):
        super().__init__()
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)

        # Create cells with random clean/dirty states
        for x in range(width):
            for y in range(height):
                estado = random.choice([0, 1])  # 0: Clean, 1: Dirty
                cell = Cell((x, y), self, estado)
                self.grid.place_agent(cell, (x, y))

        # Create agents and place them at random positions
        for i in range(self.num_agents):
            robot = RobotLimpieza(i, self)
            self.schedule.add(robot)
            x = 1
            y = 1
            self.grid.place_agent(robot, (x, y))

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


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


if __name__ == "__main__":
    width = 10
    height = 10
    num_agents = 5
    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
    server = ModularServer(
        RobotModel,
        [grid],
        "Cleaning Model",
        {"num_agents": num_agents, "width": width, "height": height}
    )
    server.port = 8521
    server.launch()
