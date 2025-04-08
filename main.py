from mesa import Agent, Model
from mesa.agent import AgentSet
from mesa.space import MultiGrid
from mesa.visualization import SolaraViz, make_plot_component, make_space_component
import random



class Predator(Agent):
    def __init__(self, unique_id, model, reproduction_chance=0.5, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.unique_id = unique_id
        self.model = model
        self.pos = None
        self.energy = 10
        self.alive = True
        self.reproductionRatio = reproduction_chance

    @classmethod
    def create_agents(cls, model, n, reproduction_chance, **kwargs):
        agents = []
        for i in range(n):
            agent = cls(i, model, reproduction_chance)
            agents.append(agent)
            x = model.rng.randrange(model.grid.width)
            y = model.rng.randrange(model.grid.height)
            model.grid.place_agent(agent, (x,y))
        return agents

    def step(self):
        print("siema Predatorze" + str(self.unique_id) + " Zyje? " + str(self.alive))
        if self.pos is None:
            return
        if self.alive == False or self.energy <= 0:
            return
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.model.rng.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.energy -= 1
        if self.model.grid[new_position][0] is not None:
            prey = self.model.grid[new_position][0]
            if isinstance(prey, Prey):
                self.energy += 10
                self.model.grid.remove_agent(prey)
                prey.alive = False
                self.model.preyCount -= 1
                if self.try_reproduction():
                    self.model.predatorCount += 1
            else:
                pass
        if self.energy <= 0:
            self.model.grid.move_agent(self, (-1,-1))
            self.model.grid.remove_agent(self)
            self.alive = False
            self.model.predatorCount -= 1

    def try_reproduction(self):
        if random.random() < self.reproductionRatio:
            new_predator = Predator(self.model.rng.randint(0,100000), self.model)
            self.model.agent_storage.add(new_predator)
            # self.model.predatorCount+=1
            self.model.grid.place_agent(new_predator, self.pos)
            return True
        return False

class Prey(Agent):
    def __init__(self, unique_id, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.unique_id = unique_id
        self.model = model
        self.pos = None
        self.alive = True

    @classmethod
    def create_agents(cls, model, n, **kwargs):
        agents = []
        for i in range(n):
            agent = cls(i, model)
            agents.append(agent)
            x = model.rng.randrange(model.grid.width)
            y = model.rng.randrange(model.grid.height)
            model.grid.place_agent(agent, (x,y))
        return agents

    def step(self):
        print("siema Preyu" + str(self.unique_id) + " Zyje? " + str(self.alive))
        if self.pos is None:
            return
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.model.rng.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class Grass(Agent):
    def __init__(self, unique_id, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.unique_id = unique_id
        self.model = model
        self.pos = None

class PredatorPreyModel(Model):
    def __init__(self, predatorNum=5, preyNum=5, width=5, height=5, seed=None, **kwargs):
        super().__init__(seed=seed)
        self.preyCount = preyNum
        self.predatorCount = predatorNum
        self.grid = MultiGrid(width, height, True)
        self.rng = random.Random(seed)
        self.agent_storage = AgentSet(agents=[], random = self.rng)
        self.agent_storage.rng = self.rng
        # Tworzenie agentów Predator
        predators = Predator.create_agents(model=self, n=predatorNum, reproduction_chance=1)
        for predator in predators:
            self.agent_storage.add(predator)

        preys = Prey.create_agents(model=self,n=preyNum)
        for prey in preys:
            self.agent_storage.add(prey)

    def step(self):
        agents_copy = self.agent_storage.shuffle(inplace=False)

        if self.predatorCount <= 0 or self.preyCount <= 0:
            model.running=False
            return

        for agent in agents_copy:
            agent.step()

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
        "max": 100,
        "step": 1,
    },
    "predatorNum": {
        "type": "SliderInt",
        "value": 5,
        "label": "Number of Foxes:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "width": {
        "type": "SliderInt",
        "value": 5,
        "label": "Width:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 5,
        "label": "Height:",
        "min": 10,
        "max": 100,
        "step": 1,
    }
}
model = PredatorPreyModel(predatorNum=5, preyNum=5, width=5, height=5)
model.step()
SpaceGraph = make_space_component(agent_portrayal)
GiniPlot = make_plot_component("Gini")
page = SolaraViz(
    model,
    components=[SpaceGraph],
    model_params=model_params,
    name="PredatorPreyModel"
)
page
