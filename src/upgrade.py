class Upgrade:
    def __init__(self, name: str, description: str, cost: int):
        self.name = name
        self.description = description
        self.effect = None
        self.cost = cost
        
    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def getCost(self):
        return self.cost

    def __repr__(self):
        return f"Upgrade(name={self.name}, description={self.description})"