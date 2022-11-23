import map
from random import randrange

class heatmap:
    def __init__(self):
        # initial position of people 
        maxPeople = 70
        self.people = [0] * len(map.states())
        for i in range(maxPeople):
           self.people[randrange(len(map.states()))]+=1

        self.move(3)


    def move(self, iterations):

        possible_transitions = map.possible_transitions()

        for i in range(len(self.people)):
            return    



heatmap1=heatmap()
