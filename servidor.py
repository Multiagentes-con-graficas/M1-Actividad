from mesa import Model, Agent
from mesa.space import MultiGrid
import random
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


class Cell(Agent):
    """Representa una celda en la cuadrícula que puede estar limpia o sucia."""

    def __init__(self, unique_id, model, estado: int):
        super().__init__(unique_id, model)
        self.estado = estado
        print(estado)


class CleanerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Obtener la posición actual del agente
        x, y = self.pos
        celda = self.model.grid.get_cell_list_contents([self.pos])

        # Limpiar la celda si está sucia
        if celda and isinstance(celda[0], Cell) and celda[0].estado == 0:
            celda[0].estado = 1

        # Mover a una nueva posición aleatoria
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


class CleaningModel(Model):
    def __init__(self, num_agents, width, height, time_limit):
        super().__init__()
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.time_limit = time_limit  # Tiempo máximo en pasos
        self.current_time = 0  # Contador de pasos actuales

        # Crear celdas en la cuadrícula con estado inicial "sucio"
        for x in range(width):
            for y in range(height):
                celda = Cell((x, y), self, random.choice([0, 1]))
                self.grid.place_agent(celda, (x, y))

        # Crear agentes de limpieza en posiciones aleatorias
        for i in range(self.num_agents):
            agent = CleanerAgent(i, self)
            self.schedule.add(agent)
            x = 1
            y = 1
            self.grid.place_agent(agent, (x, y))

    def step(self):
        if self.current_time < self.time_limit:
            self.schedule.step()
            self.current_time += 1
        else:
            print("Se alcanzó el tiempo límite de la simulación.")


def agent_portrayal(agent):
    if isinstance(agent, CleanerAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "blue",
            "Filled": True,
            "Layer": 1,
            "r": 0.5
        }
    elif isinstance(agent, Cell):
        color = "brown" if agent.estado == 0 else "green"
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
    time_limit = 100  # Tiempo máximo de pasos

    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
    server = ModularServer(
        CleaningModel,
        [grid],
        "Cleaning Model with Time Limit",
        {"num_agents": num_agents, "width": width,
            "height": height, "time_limit": time_limit}
    )
    server.port = 3001  # Puerto por defecto
    server.launch()
