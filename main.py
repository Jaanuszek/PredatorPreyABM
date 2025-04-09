import solara
from matplotlib import pyplot as plt
from mesa.visualization import SolaraViz, make_plot_component, make_space_component
from mesa.visualization.utils import update_counter

from PreyClass import Prey
from PredatorClass import Predator
from ModelClass import PredatorPreyModel
from GrassClass import Grass

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "size": 25,
    }

    if isinstance(agent, Predator):
        portrayal["color"] = "tab:red"
        portrayal["marker"] = "o"
        portrayal["zorder"] = 2
    elif isinstance(agent, Prey):
        portrayal["color"] = "tab:cyan"
        portrayal["marker"] = "o"
        portrayal["zorder"] = 2
    elif isinstance(agent, Grass):
        if agent.is_grown:
            portrayal["color"] = "tab:green"
        else:
            portrayal["color"] = "tab:brown"
            portrayal["marker"] = "s"
            portrayal["size"] = 75

    return portrayal

model_params = {
    "preyNum": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of Sheeps:",
        "min": 10,
        "max": 30,
        "step": 1,
    },
    "predatorNum": {
        "type": "SliderInt",
        "value": 5,
        "label": "Number of Foxes:",
        "min": 10,
        "max": 30,
        "step": 1,
    },
    "width": {
        "type": "SliderInt",
        "value": 5,
        "label": "Width:",
        "min": 10,
        "max": 20,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 5,
        "label": "Height:",
        "min": 10,
        "max": 20,
        "step": 1,
    },
    "reprodPredator": {
        "type": "SliderFloat",
        "value": 0.001,
        "label": "Predator reproduction Chance:",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "reprodPrey": {
        "type": "SliderFloat",
        "value": 0.001,
        "label": "Prey reproduction Chance:",
        "min": 0,
        "max": 1,
        "step": 0.01,
    }
}

@solara.component
def PopulationPlot(model):
    update_counter.get()
    fig, ax = plt.subplots()
    if hasattr(model, "datacollector"):
        data = model.datacollector.get_model_vars_dataframe()
        if not data.empty:
            ax.plot(data["Prey"], label="Prey", color="cyan")
            ax.plot(data["Predator"], label="Predator", color="red")
            ax.set_xlabel("Steps")
            ax.set_ylabel("Model count")
            ax.set_title("Population plot overt time")
            ax.legend()
    else:
        ax.text(0.5,0.5, "No data yet", ha="center")
    return solara.FigureMatplotlib(fig)

@solara.component
def WinCard(model):
    update_counter.get()
    if model.predatorCount < 0:
        return solara.Text("Preys Won!")
    elif model.preyCount < 0:
        return solara.Text("Preys Won!")
    else:
        return solara.Text("None won yet!")

# @solara.component
def wonText(model):
    update_counter.get()
    with solara.Column() as main:
        with solara.Sidebar():
            with solara.Card("Game status: "):
                WinCard(model)
    return main

model = PredatorPreyModel(reprodPredator=0.5, reprodPrey=0.5, predatorNum=5, preyNum=5, width=5, height=5, seed=None)
model.step()
SpaceGraph = make_space_component(agent_portrayal)
page = SolaraViz(
    model,
    components=[SpaceGraph, PopulationPlot, wonText],
    model_params=model_params,
    name="PredatorPreyModel"
)
page
