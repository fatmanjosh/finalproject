#!/usr/bin/env python

from Box import Box
from Robot import Robot
from Customer import Customer

def main():
    boxes = []
    boxes.append(Box("Dairy", ["milk", "oat milk", "almond milk"], ["milk", "milk", "milk" "oat milk", "almond milk"]))
    boxes.append(Box("Meat", ["bacon", "pork mince", "ham"], ["bacon", "bacon", "pork mince", "ham", "ham", "ham"]))
    boxes.append(Box("Rice", ["jasmine", "basmati", "long grain"], ["jasmine", "basmati", "long grain"]))

    replacements = ["milk","almond milk", "oat milk"]
    #replacements = ["chicken", "cow", "pig", "baby sheep"]
    myRobot = Robot(["milk"], replacements)

    if not myRobot.check_ingredients():
        myRobot.report_impossible_task()

main()



