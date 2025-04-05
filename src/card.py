class Card:
    def __init__(self, suit, rank):
        self._suit = suit
        self._rank = rank

    def getSuit(self):
        return self._suit
    
    def getRank(self):
        return self._rank

    def getValue(self):
        match self._rank:
            case "Ace":
                return 1
            case "Two":
                return 2
            case "Three":
                return 3
            case "Four":
                return 4
            case "Five":
                return 5
            case "Six":
                return 6
            case "Seven":
                return 7
            case "Eight":
                return 8
            case "Nine":
                return 9
            case "Ten":
                return 10
            case "Jack":
                return 10
            case "Queen":
                return 10
            case "King":
                return 10
            case _:
                raise ValueError("Invalid rank")

    def __lt__(self, other):
        return (self._rank < other._rank)

    def __gt__(self, other):
        return (self._rank > other._rank)

    def __le__(self, other):
        return (self._rank <= other._rank)

    def __ge__(self, other):
        return (self._rank >= other._rank)

    def __eq__(self, other):
        return (self._rank == other._rank)

    def __ne__(self, other):
        return (self._rank != other._rank)

    def __str__(self):
        return f"{self._rank} of {self._suit}"


