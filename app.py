from agents.agents import Wolf, Sheep, GrassPatch, Ground
from model import WolfSheep
from mesa.experimental.devs import ABMSimulator
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "size": 25,
    }

    if isinstance(agent, Wolf):
        portrayal["color"] = "tab:red"
        portrayal["marker"] = "o"
        portrayal["zorder"] = 2
    elif isinstance(agent, Sheep):
        portrayal["color"] = "tab:cyan"
        portrayal["marker"] = "o"
        portrayal["zorder"] = 2
    elif isinstance(agent, GrassPatch):
        if hasattr(agent, "is_grown") and agent.is_grown:
            portrayal["color"] = "tab:green"
        else:
            portrayal["color"] = "tab:brown"
            portrayal["marker"] = "s"
            portrayal["size"] = 75
    elif isinstance(agent, Ground):
        portrayal["color"] = "tab:brown"
        portrayal["marker"] = "s"
        portrayal["size"] = 75

    return portrayal


model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "grass": {
        "type": "Checkbox",
        "value": False,
        "label": "Enable Grass",
    },
    "smart_movement": {
        "type": "Checkbox",
        "value": False,
        "label": "Smart Movement",
    },
    "sheep_movement_cost": Slider("Sheep Energy Loss per Move", 1, 0, 10, 1),
    "wolf_movement_cost": Slider("Wolf Energy Loss per Move", 1, 0, 10, 1),
    "sheep_reproduction_energy_share": Slider("Sheep Energy Share for Offspring (%)", 50, 10, 100, 5),
    "wolf_reproduction_energy_share": Slider("Wolf Energy Share for Offspring (%)", 50, 10, 100, 5),
    "grass_regrowth_time": Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": Slider("Initial Sheep Population", 100, 10, 300),
    "sheep_reproduce": Slider("Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01),
    "initial_wolves": Slider("Initial Wolf Population", 10, 5, 100),
    "wolf_reproduce": Slider(
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
    ),
    "wolf_gain_from_food": Slider("Wolf Gain From Food Rate", 20, 1, 50),
    "sheep_gain_from_food": Slider("Sheep Gain From Food", 4, 1, 10),
}


def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def post_process_lines(ax):
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.9))


space_component = make_space_component(
    wolf_sheep_portrayal, draw_grid=False, post_process=post_process_space
)
lineplot_component = make_plot_component(
    {"Wolf": "tab:orange", "Sheep": "tab:cyan"},
    post_process=post_process_lines,
)
simulator = ABMSimulator()
model = WolfSheep(simulator=simulator, grass=False)
page = SolaraViz(
    model,
    components=[space_component, lineplot_component],
    model_params=model_params,
    name="Wolf Sheep",
    simulator=simulator,
)
page  # noqa
