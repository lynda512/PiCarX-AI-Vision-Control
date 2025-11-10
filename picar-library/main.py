from hardware.movement import Movement
from status.action import Action

if __name__=="__main__":
    move = Movement()

    move.forward()
    move.forward()
    move.turn(Action.LEFT, 30)
    move.turn(Action.RIGHT, 30)
    move.stop()
    move.backward()
    move.stop()