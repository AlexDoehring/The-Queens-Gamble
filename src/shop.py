class Shop:
    def __init__(self):
        self.upgrades = []
        self.powerups = []
        
    def available_upgrades(self):
        return self.upgrades
    
    def available_powerups(self):
        return self.powerups