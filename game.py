from TankBattlePVE import*
from TankBattlePVP import*


def game():
    print("Welcome to Tank Battle at Ghost Forest")
    choice=input ("1 or 2 player ? ")
    if choice== "1":
        input("1 player mode it is. (Press enter to continue)")
        PVE()

    else:
        input("2 player mode it is. (Press enter to continue)")
        PVP()


game()
