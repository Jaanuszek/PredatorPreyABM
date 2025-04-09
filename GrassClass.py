from mesa import Agent

class Grass(Agent):
    def __init__(self, unique_id, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.unique_id = unique_id
        self.model = model
        self.pos = None
