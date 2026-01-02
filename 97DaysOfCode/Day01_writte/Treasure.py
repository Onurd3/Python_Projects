from time import process_time

print('''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_______/
*******************************************************************************
''')

print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.\n")

choice1 = input(
    "Look at the map in your hand.\n"
    "Will you go right or left? (R/L): "
).lower()

if choice1 == "r":
    choice2 = input(
        "\n\nYou avoided a trap and moved forward.\n"
        "Now you see a river.\n"
        "Will you swim or wait? (swim/wait): "
    ).lower()

    if choice2 == "wait":
        choice3 = input(
            "\n\nA boat arrives and takes you across.\n"
            "You see three doors: red, blue, and yellow.\n"
            "Which one do you choose? (red/blue/yellow): "
        ).lower()

        if choice3 == "yellow":
            print("\n\nYou found the treasure. You win!")
        elif choice3 == "red":
            print("\n\nBurned by fire. Game over.")
        elif choice3 == "blue":
            print("\n\nEaten by beasts. Game over.")
        else:
            print("\nYou hesitated too long. Game over.")

    elif choice2 == "swim":
        print("\nAttacked by crocodiles. Game over.")
    else:
        print("\nYou made no decision. Game over.")

elif choice1 == "l":
    print("\nYou fell into a trap. Didn't you see it?")
    print("Game over.")

else:
    print("\nInvalid choice. Read the map properly next time.")