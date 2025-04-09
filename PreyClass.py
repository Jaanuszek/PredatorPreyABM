from mesa import Agent
import random

class Prey(Agent):
    def __init__(self, unique_id, model, reproduction_chance, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.unique_id = unique_id
        self.model = model
        self.pos = None
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
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.model.rng.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        if self.try_reproduction():
            self.model.preyCount += 1

    def try_reproduction(self):
        if self.model.rng.random() < self.reproductionRatio:
            if self.model.preyCount < 200:
                new_Prey = Prey(self.model.rng.randint(0, 100000), self.model, self.reproductionRatio)
                self.model.agent_storage.add(new_Prey)
                self.model.grid.place_agent(new_Prey, self.pos)
                return True
        return False