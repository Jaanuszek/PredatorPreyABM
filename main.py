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

    def step(self):
        print("Hello I am a scary PREDATOR " + str(self.unique_id) + "At position" + str(self.pos))
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.model.rng.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


class Prey(Agent):
    def __init__(self, unique_id, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.unique_id = unique_id
        self.model = model
        self.pos = None

    def step(self):
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
    def __init__(self, n, width, height, seed=None):
        super().__init__(seed=seed)
        self.num_agents = n  # Liczba agentów
        self.grid = MultiGrid(width, height, True)  # Siatka toroidalna
        self.rng = random.Random(seed)  # Generator losowy z opcjonalnym seedem
        self.agent_storage = AgentSet(agents=[])  # Zmieniam nazwę na self.agent_storage
        self.agent_storage.rng = self.rng  # Ustawienie generatora liczb losowych

        # Tworzenie agentów Prey
        for i in range(self.num_agents):
            a = Prey(i, self)  # Tworzenie agenta-ofiary
            self.agent_storage.add(a)  # Dodanie agenta do agent_storage
            x = self.rng.randrange(self.grid.width)
            y = self.rng.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))  # Umieszczenie agenta w siatce
            b = Predator(i, self)
            self.agent_storage.add(b)  # Dodanie agenta do agent_storage
            xPredator = self.rng.randrange(self.grid.width)
            yPredator = self.rng.randrange(self.grid.height)
            self.grid.place_agent(b, (xPredator, yPredator))  # Umieszczenie agenta w siatce

    def step(self):
        # self.agent_storage.step()  # Przeprowadzenie kroku dla wszystkich agentów
        for agent in self.agent_storage:  # Iteracja przez agentów
            agent.step()  # Wywołanie metody step każdego agenta
def plot_agents(model, width = 10, height = 10):
    grid = model.grid
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, grid.width - 0.5)
    ax.set_ylim(-0.5, grid.height - 0.5)
    ax.set_xticks(range(width))
    ax.set_yticks(range(height))
    ax.grid(True)

    # model.grid.plot(ax)
    for agent in model.agent_storage:
        x, y = agent.pos
        if isinstance(agent,Prey):
            ax.plot(x, y, "o", color="blue")
        if isinstance(agent,Predator):
            ax.plot(x, y, "o", color="red")
        # ax.scatter(x, y, color="red")
    plt.gca().invert_yaxis()
    plt.show()
# Inicjalizacja modelu
model = PredatorPreyModel(10, 10, 10)
for i in range(10):
    model.step()
    plot_agents(model)
    time.sleep(2)
