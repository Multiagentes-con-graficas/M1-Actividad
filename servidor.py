from robot_limpieza import RobotModel, agent_portrayal, FinalStatsText
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

if __name__ == "__main__":
    modelParams = {
        "width": Slider(
            "With of the grid",
            value=10,
            min_value=5,
            max_value=20,
            step=1,
            description="With of the grid (M)"
        ),
        "height": Slider(
            "Height of the grid",
            value=10,
            min_value=5,
            max_value=20,
            step=1,
            description="Height of the grid (N)"
        ),
        "num_agents": Slider(
            "Number of robots",
            value=1,
            min_value=1,
            max_value=10,
            step=1,
            description="Number of robots in the grid"
        ),
        "percentage_dirt": Slider(
            "Dirty cells percentage",
            value=0.3,
            min_value=0.1,
            max_value=1,
            step=0.1,
            description="Dirty cells percentage in the grid"
        ),
        "time_ejection": Slider(
            "Time ejection",
            value=60,
            min_value=10,
            max_value=300,
            step=10,
            description="Time ejection in steps"
        )
    }

    grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

    chart = ChartModule(
        [
            {"Label": "Celdas Limpias", "Color": "Green"},
            {"Label": "Celdas Sucias", "Color": "Red"},
        ],
        data_collector_name='datacollector'
    )

    final_stats_text = FinalStatsText()

    server = ModularServer(
        RobotModel,
        [grid, chart, final_stats_text],
        "Cleaning Model",
        modelParams
    )
    server.port = 8522
    server.launch()
