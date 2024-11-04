from robot_limpieza import RobotModel, agent_portrayal
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

if __name__ == "__main__":
    width = 20
    height = 20
    num_agents = 5
    percentage_dirt = 0
    time_ejection = 100
    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
    server = ModularServer(
        RobotModel,
        [grid],
        "Cleaning Model",
        {"num_agents": num_agents, "width": width,
            "height": height, "time_ejection": time_ejection, "percentage_dirt": percentage_dirt}
    )
    server.port = 8521
    server.launch()
