from mesa import Agent, Model
from mesa.agent import AgentSet
from mesa.space import MultiGrid
import random
import matplotlib.pyplot as plt
import time


class Predator(Agent):
    def __init__(self, unique_id, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.unique_id = unique_id
        self.model = model
        self.pos = None
        self.energy = 10

    def step(self):
        if self.pos is None:
            return
        print ("Predator with id: " + str(self.unique_id) + ", energy: " + str(self.energy))
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
                self.model.agent_storage.remove(prey)
                self.model.preyCount -= 1

            else:
                pass
        if self.energy <= 0:
            self.model.grid.move_agent(self, (-1,-1))
            self.model.grid.remove_agent(self)
            self.model.agent_storage.remove(self)
            self.model.predatorCount -= 1

class Prey(Agent):
    def __init__(self, unique_id, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.unique_id = unique_id
        self.model = model
        self.pos = None

    def step(self):
        if self.pos is None:
            return
        print("Hello I am a scary PREY " + str(self.unique_id) + "At position" + str(self.pos))
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
    def __init__(self, predatorNum, preyNum, width, height, seed=None):
        super().__init__(seed=seed)
        self.preyCount = preyNum
        self.predatorCount = predatorNum
        self.grid = MultiGrid(width, height, True)
        self.rng = random.Random(seed)
        self.agent_storage = AgentSet(agents=[], random = self.rng)
        self.agent_storage.rng = self.rng
        # Tworzenie agentów Predator
        for i in range(self.predatorCount):
            predator = Predator(i, self)
            self.agent_storage.add(predator)
            x = self.rng.randrange(self.grid.width)
            y = self.rng.randrange(self.grid.height)
            self.grid.place_agent(predator, (x,y))
        #Tworzenie agentów Prey
        for i in range(self.preyCount):
            prey = Prey(i, self)
            self.agent_storage.add(prey)
            x = self.rng.randrange(self.grid.width)
            y = self.rng.randrange(self.grid.height)
            self.grid.place_agent(prey, (x,y))

    def step(self):
        for agent in list(self.agent_storage):
            agent.step()

def plot_agents(model, width = 10, height = 10):
    grid = model.grid
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, grid.width - 0.5)
    ax.set_ylim(-0.5, grid.height - 0.5)
    ax.set_xticks(range(width))
    ax.set_yticks(range(height))
    ax.grid(True)

    # model.grid.plot(ax)
    for agent in list(model.agent_storage):
        x, y = agent.pos
        if isinstance(agent,Prey):
            ax.plot(x, y, "o", color="blue")
        if isinstance(agent,Predator):
            ax.plot(x, y, "o", color="red")
    plt.gca().invert_yaxis()
    plt.show()
# Inicjalizacja modelu
model = PredatorPreyModel(10, 10, 10, 10)
for i in range(100):
    model.step()
    plot_agents(model)
    if model.predatorCount <= 0:
        print("No predators, Preys won")
        break
    if model.preyCount <= 0:
        print("No Preys, predators won")
        break
    time.sleep(0.5)
