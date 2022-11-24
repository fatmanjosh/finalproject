#!/usr/bin/env python3
import map
from random import randrange
import random

class heatmap:
    # will not have many people in the store so I'll scrap the vector frequency
    def __init__(self, nrPeople):
        # initial position of people - I think about 40-60 people is good
        self.people = []
        for i in range(nrPeople):
           self.people.append (randrange(0,len(map.states())-1,1))

        self.possible_transitions = map.possible_transitions()


    def move(self, iterations):
        possible_transitions = self.possible_transitions
        people = self.people
        for _ in range(iterations):
            for i in range(len(people)):
                if(possible_transitions["s" + str(people[i])] != ['TERMINAL']):
                    rn = random.choice(possible_transitions["s" + str(people[i])])

                    # required python 3.10 +
                    # match random.choice(possible_transitions["s" + str(people[i])]):
                    #     case 'LEFT':
                    #         people[i] -= 1
                    #     case 'RIGHT':
                    #         people[i] += 1
                    #     case 'UP':
                    #         people[i] = self.wackMoveUp(people[i])
                    #     case 'DOWN':
                    #         people[i] = self.wackMoveDown(people[i])
                    #     case _:
                    #         print ("Hello I am the guy that asked - debugger") 

                    if (rn == 'LEFT'):
                        people[i] -=1
                        next
                    if(rn == 'RIGHT'):
                        people[i] +=1
                        next
                    if(rn == 'DOWN'):
                        people[i] = self.moveDown("s" + str(people[i]))
                        next
                    if(rn == 'UP'):
                        people[i] = self.moveUp("s" + str(people[i]))
                        next

                else:
                    people[i] = randrange(0,len(map.states())-1,1) # assume they finish the shopping when they get to term state and summon new ones
        
        return people

    #this is the function that you should call when you get to a goal state and you need to update the heatmap and recalculate the policy
    #iterations = number of steps the robot moves (would make sense)
    def stateUncertenty (self, iterations):
        self.people = self.move(iterations)

        return self.people

    def moveUp(self,state):
        allStates = map.states()
        x = allStates[state][0]
        y = allStates[state][1] + 1
        for nextState in allStates:
            if(allStates[nextState][0] == x and allStates[nextState][1] == y):
                return int(''.join(filter(str.isdigit, nextState))) 

    def moveDown(self,state):
        allStates = map.states()
        x = allStates[state][0]
        y = allStates[state][1] - 1
        for nextState in allStates:
            if(allStates[nextState][0] == x and allStates[nextState][1] == y):
                return int(''.join(filter(str.isdigit, nextState)))

heatmap = heatmap(60)