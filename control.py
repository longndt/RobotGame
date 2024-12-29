# TO-DO: Implement code for function "run"
# 1)  robot.direction = "X"    => set initial head direction of robot (X: up, down, left, right)
# Ex: robot.direction = "up"

# 2)  robot.turn("X")          => change robot turn direction (X: up, left, right, down)
# Ex: robot.turn("right")

# 3)  robot.go(X)              => define number of steps to go (X: 1,2,3,4,....)
# Ex: robot.go(3)

# START: Press "Start Game" button
def run(robot):
    robot.direction = "left"
    robot.go(4)
    robot.turn("down")
    robot.go(1)
    robot.turn("right")
    robot.go(6)
    robot.turn("left")
    robot.go(4)

