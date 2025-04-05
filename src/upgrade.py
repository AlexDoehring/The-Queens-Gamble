class Upgrade:
    def __init__(self, name: str, description: str, cost: int):
        self.name = name
        self.description = description
        self.effect = None
        self.cost = cost
        self.level = 0
        self.max_level = 5
        
    def increase_level(self):
        if self.level < self.max_level:
            self.level += 1
            return True
        return False
        
    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def getCost(self):
        return self.cost

    def __repr__(self):
        return f"Upgrade(name={self.name}, description={self.description})"