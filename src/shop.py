from upgrade import Upgrade
from powerup import PowerUp

class Shop:
    def __init__(self):
        self.upgrades = [
            Upgrade("Luck", "decreases opponents chance of capturing a piece", 5),
            Upgrade("Bounty", "increases reward of each piece's capture", 10)
        ]
        
        self.powerups = [
            PowerUp("Takeback", "allows you to take back a move", 5),
            PowerUp("Redo", "allows you to redo a lost Blackjack game", 10),
            PowerUp("Skip", "allows you to skip the opponent's turn", 15)
        ]
        
    def available_upgrades(self):
        return self.upgrades
    
    def available_powerups(self):
        return self.powerups