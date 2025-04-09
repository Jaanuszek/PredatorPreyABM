from mesa import Model
from mesa.agent import AgentSet
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random
from PredatorClass import Predator
from PreyClass import Prey

class PredatorPreyModel(Model):
    def __init__(self, reprodPredator=0.1, reprodPrey=0.1, predatorNum=5, preyNum=5, width=5, height=5, seed=None, **kwargs):
        super().__init__(seed=seed)
        self.preyCount = preyNum
        self.predatorCount = predatorNum
        self.grid = MultiGrid(width, height, True)
        self.rng = random.Random(seed)
        self.agent_storage = AgentSet(agents=[], random = self.rng)
        self.agent_storage.rng = self.rng
        self.reproductionPredatorRatio = reprodPredator
        self.reproductionPreyRatio = reprodPrey
        self.datacollector = DataCollector(
            model_reporters={
                "Prey": lambda m: sum(1 for a in m.agent_storage if isinstance(a,Prey)),
                "Predator": lambda m: sum (1 for a in m.agent_storage if isinstance(a, Predator))
            }
        )
        # Tworzenie agentów Predator
        predators = Predator.create_agents(model=self, n=predatorNum, reproduction_chance=self.reproductionPredatorRatio)
        for predator in predators:
            self.agent_storage.add(predator)

        preys = Prey.create_agents(model=self,n=preyNum, reproduction_chance = self.reproductionPreyRatio)
        for prey in preys:
            self.agent_storage.add(prey)

    def step(self):
        self.datacollector.collect(self)
        agents_copy = self.agent_storage.shuffle(inplace=False)
        print(str(self.predatorCount) + " " + str(self.preyCount))
        if self.predatorCount <= 0 or self.preyCount <= 0:
            self.running=False
            if (self.predatorCount > 0):
                print ("Predators Won!")
            else:
                print ("Preys Won!")
            return

        for agent in agents_copy:
            agent.step()
