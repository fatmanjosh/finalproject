from Box import Box
from Robot import Robot
from Customer import Customer

def main():
    boxes = []
    boxes.append(Box("Dairy", ["milk"], ["milk", "milk"]))

    replacements = ["milk","almond milk", "oat milk"]
    myRobot = Robot(["milk"], replacements)

    if not myRobot.check_ingredients():
        myRobot.report_impossible_task()

main()



