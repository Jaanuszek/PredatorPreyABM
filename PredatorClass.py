from mesa import Agent
import random
from PreyClass import Prey

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
                self.model.agent_storage.remove(prey)
                if self.try_reproduction():
                    self.model.predatorCount += 1
            else:
                pass
        if self.energy <= 0:
            self.model.grid.move_agent(self, (-1,-1))
            self.model.grid.remove_agent(self)
            self.model.agent_storage.remove(self)
            self.alive = False
            self.model.predatorCount -= 1

    def try_reproduction(self):
        if random.random() < self.reproductionRatio:
            if self.model.predatorCount < 200:
                new_predator = Predator(self.model.rng.randint(0,100000), self.model)
                self.model.agent_storage.add(new_predator)
                self.model.grid.place_agent(new_predator, self.pos)
                return True
        return False
